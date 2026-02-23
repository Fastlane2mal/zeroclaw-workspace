#!/usr/bin/env python3
"""
Frank's Meal Planning Engine
Generates weekly meal plans based on available pantry items
Formats output for Telegram
"""
import sqlite3
from datetime import datetime, timedelta
import json

DB_PATH = "food/food.db"

class FrankPlanner:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def get_available_recipes(self):
        """Get recipes that can be made with available pantry items"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get all recipes and check if we have ingredients
        c.execute("""
            SELECT DISTINCT r.id, r.name, r.meal_type, r.description
            FROM recipes r
            ORDER BY r.meal_type, r.name
        """)
        
        recipes = c.fetchall()
        available = []
        
        for recipe_id, name, meal_type, description in recipes:
            # Check if all ingredients are in pantry
            c.execute("""
                SELECT ri.food_id, ri.quantity_grams, f.name
                FROM recipe_ingredients ri
                JOIN foods f ON ri.food_id = f.id
                WHERE ri.recipe_id = ?
            """, (recipe_id,))
            
            ingredients = c.fetchall()
            can_make = True
            
            for food_id, needed_qty, food_name in ingredients:
                c.execute("SELECT quantity_grams FROM store_cupboard WHERE food_id = ?", (food_id,))
                pantry = c.fetchone()
                
                if not pantry or pantry[0] < needed_qty:
                    can_make = False
                    break
            
            if can_make:
                available.append({
                    'id': recipe_id,
                    'name': name,
                    'meal_type': meal_type,
                    'description': description
                })
        
        conn.close()
        return available
    
    def get_recipe_details(self, recipe_id):
        """Get full recipe details with ingredients"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT name, meal_type, prep_time_mins, cook_time_mins FROM recipes WHERE id = ?", (recipe_id,))
        recipe = c.fetchone()
        
        c.execute("""
            SELECT f.name, ri.quantity_grams, f.calories_per_100g, f.protein_g, f.carbs_g, f.fat_g
            FROM recipe_ingredients ri
            JOIN foods f ON ri.food_id = f.id
            WHERE ri.recipe_id = ?
        """, (recipe_id,))
        
        ingredients = c.fetchall()
        conn.close()
        
        return {
            'name': recipe[0],
            'meal_type': recipe[1],
            'prep_time': recipe[2],
            'cook_time': recipe[3],
            'ingredients': ingredients
        }
    
    def generate_weekly_plan(self):
        """Generate a weekly meal plan"""
        available = self.get_available_recipes()
        
        if not available:
            return None, "❌ No recipes can be made with current pantry items"
        
        # Group by meal type
        by_type = {}
        for recipe in available:
            meal_type = recipe['meal_type']
            if meal_type not in by_type:
                by_type[meal_type] = []
            by_type[meal_type].append(recipe)
        
        # Simple plan: pick one recipe per day
        plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Rotate through available recipes
        dinner_recipes = by_type.get('dinner', [])
        lunch_recipes = by_type.get('lunch', [])
        breakfast_recipes = by_type.get('breakfast', [])
        
        for i, day in enumerate(days):
            plan[day] = {
                'breakfast': breakfast_recipes[i % len(breakfast_recipes)] if breakfast_recipes else None,
                'lunch': lunch_recipes[i % len(lunch_recipes)] if lunch_recipes else None,
                'dinner': dinner_recipes[i % len(dinner_recipes)] if dinner_recipes else None,
            }
        
        return plan, None
    
    def calculate_shopping_list(self, plan):
        """Calculate what needs to be bought"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        needed = {}  # food_id -> total_quantity_needed
        
        # Sum up all ingredients needed for the week
        for day, meals in plan.items():
            for meal_type, recipe in meals.items():
                if recipe:
                    c.execute("""
                        SELECT food_id, quantity_grams
                        FROM recipe_ingredients
                        WHERE recipe_id = ?
                    """, (recipe['id'],))
                    
                    for food_id, qty in c.fetchall():
                        needed[food_id] = needed.get(food_id, 0) + qty
        
        # Calculate what to buy
        shopping = {}
        for food_id, total_needed in needed.items():
            c.execute("SELECT quantity_grams FROM store_cupboard WHERE food_id = ?", (food_id,))
            pantry = c.fetchone()
            pantry_qty = pantry[0] if pantry else 0
            
            if total_needed > pantry_qty:
                to_buy = total_needed - pantry_qty
                c.execute("SELECT name, category FROM foods WHERE id = ?", (food_id,))
                food = c.fetchone()
                shopping[food[0]] = {
                    'category': food[1],
                    'quantity': to_buy,
                    'pantry': pantry_qty,
                    'needed': total_needed
                }
        
        conn.close()
        return shopping
    
    def format_plan_message(self, plan, shopping_list):
        """Format meal plan and shopping list for Telegram"""
        message = "🍽️ **Weekly Meal Plan**\n"
        message += f"Generated: {datetime.now().strftime('%A, %B %d, %Y')}\n\n"
        
        # Meal plan
        message += "**Meal Schedule:**\n"
        for day, meals in plan.items():
            message += f"\n*{day}:*\n"
            if meals['breakfast']:
                message += f"  🌅 Breakfast: {meals['breakfast']['name']}\n"
            if meals['lunch']:
                message += f"  🥗 Lunch: {meals['lunch']['name']}\n"
            if meals['dinner']:
                message += f"  🍽️ Dinner: {meals['dinner']['name']}\n"
        
        # Shopping list
        message += "\n\n**🛒 Shopping List:**\n"
        if shopping_list:
            by_category = {}
            for item, details in shopping_list.items():
                cat = details['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append((item, details['quantity']))
            
            for category in sorted(by_category.keys()):
                message += f"\n*{category.capitalize()}:*\n"
                for item, qty in sorted(by_category[category]):
                    message += f"  ☐ {item}: {qty:.0f}g\n"
        else:
            message += "  ✓ Everything you need is already in the pantry!\n"
        
        return message
    
    def generate_plan(self):
        """Main method: generate and format plan"""
        plan, error = self.generate_weekly_plan()
        
        if error:
            return error
        
        shopping_list = self.calculate_shopping_list(plan)
        message = self.format_plan_message(plan, shopping_list)
        
        return message


# Test
if __name__ == "__main__":
    frank = FrankPlanner()
    result = frank.generate_plan()
    print(result)
