#!/usr/bin/env python3
"""
Frank's Meal Planner - Generates weekly meal plans based on pantry and preferences
Formats data for Telegram delivery
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random

class FrankMealPlanner:
    def __init__(self, db_path: str = "food/food.db"):
        self.db_path = db_path
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    def get_available_recipes(self) -> List[Dict]:
        """Get recipes that can be made with pantry items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all recipes and check ingredient availability
        cursor.execute('''
            SELECT DISTINCT r.id, r.name, r.prep_time_mins, r.cook_time_mins
            FROM recipes r
            ORDER BY r.name
        ''')
        
        recipes = cursor.fetchall()
        available = []
        
        for recipe_id, name, prep_time, cook_time in recipes:
            # Check if all ingredients are in pantry
            cursor.execute('''
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END) as in_pantry
                FROM recipe_ingredients ri
                LEFT JOIN pantry p ON ri.food_id = p.food_id
                WHERE ri.recipe_id = ?
            ''', (recipe_id,))
            
            total, in_pantry = cursor.fetchone()
            
            # Consider recipe available if 80% of ingredients are in pantry
            if in_pantry and (in_pantry / total >= 0.8):
                available.append({
                    "id": recipe_id,
                    "name": name,
                    "prep_time": prep_time,
                    "cook_time": cook_time,
                    "coverage": in_pantry / total
                })
        
        conn.close()
        return available
    
    def get_recipe_details(self, recipe_id: int) -> Dict:
        """Get detailed recipe information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, prep_time_mins, cook_time_mins FROM recipes WHERE id = ?', (recipe_id,))
        recipe = cursor.fetchone()
        
        cursor.execute('''
            SELECT f.name, ri.quantity, ri.unit
            FROM recipe_ingredients ri
            JOIN foods f ON ri.food_id = f.id
            WHERE ri.recipe_id = ?
            ORDER BY f.category, f.name
        ''', (recipe_id,))
        
        ingredients = cursor.fetchall()
        conn.close()
        
        return {
            "name": recipe[0],
            "prep_time": recipe[1],
            "cook_time": recipe[2],
            "ingredients": ingredients
        }
    
    def generate_weekly_plan(self, user_id: int = 1) -> Dict:
        """Generate a 7-day meal plan"""
        available_recipes = self.get_available_recipes()
        
        if not available_recipes:
            return {
                "success": False,
                "message": "Not enough pantry items to create a meal plan. Please update your pantry!"
            }
        
        plan = {
            "week_start": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "days": {}
        }
        
        # Select recipes for each day (try to vary)
        used_recipes = set()
        for day in self.days:
            # Get available recipes not used yet, or reuse if necessary
            available = [r for r in available_recipes if r["id"] not in used_recipes]
            if not available:
                available = available_recipes
            
            selected = random.choice(available)
            used_recipes.add(selected["id"])
            
            recipe_details = self.get_recipe_details(selected["id"])
            
            plan["days"][day] = {
                "recipe": recipe_details["name"],
                "recipe_id": selected["id"],
                "prep_time": recipe_details["prep_time"],
                "cook_time": recipe_details["cook_time"],
                "ingredients": recipe_details["ingredients"]
            }
        
        return plan
    
    def generate_shopping_list(self, plan: Dict) -> Dict:
        """Generate shopping list from meal plan"""
        shopping_list = {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for day, meal_data in plan["days"].items():
            for ingredient_name, quantity, unit in meal_data["ingredients"]:
                # Check if in pantry
                cursor.execute('''
                    SELECT p.quantity, p.unit FROM pantry p
                    JOIN foods f ON p.food_id = f.id
                    WHERE LOWER(f.name) = LOWER(?)
                ''', (ingredient_name,))
                
                pantry_item = cursor.fetchone()
                
                if not pantry_item:
                    # Need to buy
                    key = ingredient_name
                    if key not in shopping_list:
                        shopping_list[key] = {"quantity": 0, "unit": unit}
                    shopping_list[key]["quantity"] += quantity
        
        conn.close()
        
        return {
            "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "items": shopping_list

        }
    
    def format_plan_for_telegram(self, plan: Dict, shopping_list: Dict) -> str:
        """Format meal plan and shopping list for Telegram message"""
        
        output = "📅 **Weekly Meal Plan**\n"
        output += f"Week starting: {plan['week_start']}\n"
        output += "─" * 40 + "\n\n"
        
        for day in self.days:
            if day in plan["days"]:
                meal = plan["days"][day]
                output += f"*{day}*\n"
                output += f"  🍽️ {meal['recipe']}\n"
                output += f"  ⏱️ Prep: {meal['prep_time']}min | Cook: {meal['cook_time']}min\n"
                output += "\n"
        
        output += "─" * 40 + "\n\n"
        output += "🛒 **Shopping List**\n"
        output += f"Generated: {shopping_list['generated_date']}\n\n"
        
        if shopping_list["items"]:
            for item, details in sorted(shopping_list["items"].items()):
                output += f"  ☐ {item}: {details['quantity']} {details['unit']}\n"
        else:
            output += "  ✓ All ingredients in pantry!\n"
        
        return output
    
    def save_plan_to_db(self, plan: Dict, user_id: int = 1):
        """Save meal plan to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        week_start = plan["week_start"]
        
        for day_index, day in enumerate(self.days):
            if day in plan["days"]:
                meal = plan["days"][day]
                meal_date = datetime.strptime(week_start, "%Y-%m-%d") + timedelta(days=day_index)
                
                cursor.execute('''
                    INSERT INTO meals (user_id, recipe_id, meal_date, meal_type)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, meal["recipe_id"], meal_date.strftime("%Y-%m-%d"), "dinner"))
        
        conn.commit()
        conn.close()


def generate_and_send_plan():
    """Main function to generate plan and prepare for Telegram"""
    frank = FrankMealPlanner()
    
    # Generate plan
    plan = frank.generate_weekly_plan()
    
    if not plan.get("success", True):
        return plan["message"]
    
    # Generate shopping list
    shopping_list = frank.generate_shopping_list(plan)
    
    # Format for Telegram
    telegram_message = frank.format_plan_for_telegram(plan, shopping_list)
    
    # Save to database
    frank.save_plan_to_db(plan)
    
    return telegram_message


if __name__ == "__main__":
    message = generate_and_send_plan()
    print(message)
