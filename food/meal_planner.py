#!/usr/bin/env python3
"""
Frank's Meal Planner - Database management and Telegram integration
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / 'food.db'
SCHEMA_PATH = Path(__file__).parent / 'schema.sql'
SEED_PATH = Path(__file__).parent / 'seed_data.sql'


class FoodDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def init_db(self):
        """Initialize database with schema"""
        self.connect()
        with open(SCHEMA_PATH, 'r') as f:
            self.conn.executescript(f.read())
        self.conn.commit()
        print(f"✓ Database initialized at {self.db_path}")
    
    def seed_db(self):
        """Populate database with test data"""
        self.connect()
        with open(SEED_PATH, 'r') as f:
            self.conn.executescript(f.read())
        self.conn.commit()
        print("✓ Database seeded with test data")
    
    def add_to_store_cupboard(self, food_name, quantity, unit):
        """Add or update item in store cupboard"""
        self.connect()
        cursor = self.conn.cursor()
        
        # Get food ID
        cursor.execute("SELECT id FROM foods WHERE name = ?", (food_name,))
        result = cursor.fetchone()
        
        if not result:
            return {"error": f"Food '{food_name}' not found"}
        
        food_id = result[0]
        
        # Check if already in cupboard
        cursor.execute("SELECT id FROM store_cupboard WHERE food_id = ?", (food_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute(
                "UPDATE store_cupboard SET quantity = quantity + ?, last_updated = CURRENT_TIMESTAMP WHERE food_id = ?",
                (quantity, food_id)
            )
        else:
            cursor.execute(
                "INSERT INTO store_cupboard (food_id, quantity, unit) VALUES (?, ?, ?)",
                (food_id, quantity, unit)
            )
        
        self.conn.commit()
        return {"success": f"Added {quantity}{unit} of {food_name} to store cupboard"}
    
    def get_store_cupboard(self):
        """Get current store cupboard inventory"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT f.name, sc.quantity, sc.unit, sc.last_updated
            FROM store_cupboard sc
            JOIN foods f ON sc.food_id = f.id
            ORDER BY f.category, f.name
        """)
        
        items = cursor.fetchall()
        self.close()
        
        return items
    
    def get_meal_plan_for_week(self, user_id=1):
        """Get meal plan for the current week"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT m.day_of_week, m.meal_type, r.name, r.prep_time_mins, r.cook_time_mins
            FROM meals m
            JOIN meal_plans mp ON m.meal_plan_id = mp.id
            JOIN recipes r ON m.recipe_id = r.id
            WHERE mp.user_id = ? AND m.meal_plan_id = (
                SELECT id FROM meal_plans WHERE user_id = ? ORDER BY week_start_date DESC LIMIT 1
            )
            ORDER BY CASE 
                WHEN m.day_of_week = 'Monday' THEN 1
                WHEN m.day_of_week = 'Tuesday' THEN 2
                WHEN m.day_of_week = 'Wednesday' THEN 3
                WHEN m.day_of_week = 'Thursday' THEN 4
                WHEN m.day_of_week = 'Friday' THEN 5
                WHEN m.day_of_week = 'Saturday' THEN 6
                WHEN m.day_of_week = 'Sunday' THEN 7
            END,
            CASE WHEN m.meal_type = 'Breakfast' THEN 1 WHEN m.meal_type = 'Lunch' THEN 2 ELSE 3 END
        """, (user_id, user_id))
        
        meals = cursor.fetchall()
        self.close()
        
        return meals
    
    def generate_shopping_list(self, user_id=1):
        """Generate shopping list from meal plan"""
        self.connect()
        cursor = self.conn.cursor()
        
        # Get latest meal plan
        cursor.execute("""
            SELECT id FROM meal_plans WHERE user_id = ? ORDER BY week_start_date DESC LIMIT 1
        """, (user_id,))
        
        plan_result = cursor.fetchone()
        if not plan_result:
            return {"error": "No meal plan found"}
        
        meal_plan_id = plan_result[0]
        
        # Get all ingredients needed for the meal plan
        cursor.execute("""
            SELECT f.name, SUM(ri.quantity) as total_qty, ri.unit
            FROM meals m
            JOIN recipe_ingredients ri ON m.recipe_id = ri.recipe_id
            JOIN foods f ON ri.food_id = f.id
            WHERE m.meal_plan_id = ?
            GROUP BY f.id, f.name, ri.unit
            ORDER BY f.category, f.name
        """, (meal_plan_id,))
        
        items = cursor.fetchall()
        self.close()
        
        return items
    
    def format_meal_plan_message(self, user_id=1):
        """Format meal plan for Telegram message"""
        meals = self.get_meal_plan_for_week(user_id)
        
        if not meals:
            return "No meal plan available"
        
        message = "📅 *Weekly Meal Plan*\n\n"
        current_day = None
        
        for meal in meals:
            day, meal_type, recipe, prep, cook = meal
            
            if day != current_day:
                message += f"\n*{day}*\n"
                current_day = day
            
            message += f"  {meal_type}: {recipe} ({prep}min prep, {cook}min cook)\n"
        
        return message
    
    def format_shopping_list_message(self, user_id=1):
        """Format shopping list for Telegram message"""
        items = self.generate_shopping_list(user_id)
        
        if isinstance(items, dict) and "error" in items:
            return items["error"]
        
        message = "🛒 *Weekly Shopping List*\n\n"
        
        for item in items:
            name, qty, unit = item
            message += f"  ☐ {name}: {qty}{unit}\n"
        
        return message
    
    def format_store_cupboard_message(self):
        """Format store cupboard for Telegram message"""
        items = self.get_store_cupboard()
        
        message = "🥫 *Store Cupboard Inventory*\n\n"
        
        current_category = None
        for item in items:
            name, qty, unit, updated = item
            # Extract category from name or use generic
            if current_category != name.split()[0]:
                current_category = name.split()[0]
            
            message += f"  {name}: {qty}{unit}\n"
        
        return message


def init_fresh_database():
    """Initialize a fresh database with schema and seed data"""
    db = FoodDatabase()
    db.init_db()
    db.seed_db()
    print("✓ Database ready!")


def get_weekly_update(user_id=1):
    """Get formatted meal plan and shopping list for weekly update"""
    db = FoodDatabase()
    
    meal_plan = db.format_meal_plan_message(user_id)
    shopping_list = db.format_shopping_list_message(user_id)
    
    db.close()
    
    return f"{meal_plan}\n\n{shopping_list}"


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            init_fresh_database()
        elif command == "meal-plan":
            db = FoodDatabase()
            print(db.format_meal_plan_message())
            db.close()
        elif command == "shopping-list":
            db = FoodDatabase()
            print(db.format_shopping_list_message())
            db.close()
        elif command == "cupboard":
            db = FoodDatabase()
            print(db.format_store_cupboard_message())
            db.close()
        elif command == "weekly-update":
            print(get_weekly_update())
        elif command == "add-cupboard" and len(sys.argv) >= 5:
            food_name = sys.argv[2]
            quantity = float(sys.argv[3])
            unit = sys.argv[4]
            db = FoodDatabase()
            result = db.add_to_store_cupboard(food_name, quantity, unit)
            print(json.dumps(result))
            db.close()
        else:
            print("Usage: python meal_planner.py [init|meal-plan|shopping-list|cupboard|weekly-update|add-cupboard <food> <qty> <unit>]")
    else:
        print("Meal Planner initialized. Use with commands.")
