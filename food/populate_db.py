#!/usr/bin/env python3
"""
Populate food.db with healthy recipes and test data
"""
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "food/food.db"

def populate_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users
    c.execute("""
        INSERT INTO users (name, dietary_restrictions, health_conditions, preferences)
        VALUES 
        ('User 1', 'vegetarian', 'none', 'Mediterranean diet'),
        ('User 2', 'none', 'diabetes', 'low-sugar meals')
    """)
    
    # Create food items with nutritional info
    foods = [
        # Proteins
        ('Chicken Breast', 'protein', 165, 31, 0, 3.6, 0),
        ('Salmon', 'protein', 208, 20, 0, 13, 0),
        ('Eggs', 'protein', 155, 13, 1.1, 11, 0),
        ('Lentils', 'protein', 116, 9, 20, 0.4, 8),
        
        # Vegetables
        ('Broccoli', 'vegetable', 34, 2.8, 7, 0.4, 2.4),
        ('Spinach', 'vegetable', 23, 2.9, 3.6, 0.4, 2.2),
        ('Carrots', 'vegetable', 41, 0.9, 10, 0.2, 2.8),
        ('Bell Pepper', 'vegetable', 31, 1, 7, 0.3, 2.2),
        ('Tomato', 'vegetable', 18, 0.9, 3.9, 0.2, 1.2),
        
        # Grains
        ('Brown Rice', 'grain', 111, 2.6, 23, 0.9, 1.8),
        ('Quinoa', 'grain', 120, 4.4, 21, 1.6, 2.8),
        ('Whole Wheat Bread', 'grain', 100, 3.6, 18, 1.4, 2.7),
        
        # Dairy
        ('Greek Yogurt', 'dairy', 59, 10, 3.3, 0.4, 0),
        ('Milk', 'dairy', 61, 3.2, 4.8, 3.3, 0),
        ('Cheddar Cheese', 'dairy', 403, 23, 3.3, 33, 0),
        
        # Fruits
        ('Apple', 'fruit', 52, 0.3, 14, 0.2, 2.4),
        ('Banana', 'fruit', 89, 1.1, 23, 0.3, 2.6),
        ('Blueberries', 'fruit', 57, 0.7, 14, 0.3, 2.4),
        
        # Oils & Condiments
        ('Olive Oil', 'oil', 884, 0, 0, 100, 0),
        ('Garlic', 'condiment', 149, 6.4, 33, 0.5, 2.1),
    ]
    
    for name, category, cal, protein, carbs, fat, fiber in foods:
        c.execute("""
            INSERT INTO foods (name, category, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, category, cal, protein, carbs, fat, fiber))
    
    # Create recipes
    recipes = [
        ('Grilled Chicken with Broccoli', 20, 30, 'High protein, low carb'),
        ('Salmon & Quinoa Bowl', 25, 35, 'Omega-3 rich, balanced'),
        ('Vegetable Stir Fry', 15, 25, 'Vegetarian, quick'),
        ('Lentil Soup', 30, 40, 'High fiber, plant-based'),
        ('Greek Salad with Feta', 10, 20, 'Light, Mediterranean'),
        ('Egg White Omelette', 10, 15, 'Low calorie, high protein'),
        ('Overnight Oats', 15, 20, 'Convenient, balanced'),
    ]
    
    recipe_ids = {}
    for name, prep_time, cook_time, description in recipes:
        c.execute("""
            INSERT INTO recipes (name, prep_time_minutes, cook_time_minutes, description, difficulty)
            VALUES (?, ?, ?, ?, ?)
        """, (name, prep_time, cook_time, description, 'easy'))
        recipe_ids[name] = c.lastrowid
    
    # Link recipes to ingredients
    recipe_ingredients = [
        ('Grilled Chicken with Broccoli', [('Chicken Breast', 150), ('Broccoli', 200), ('Olive Oil', 10)]),
        ('Salmon & Quinoa Bowl', [('Salmon', 150), ('Quinoa', 100), ('Spinach', 100), ('Olive Oil', 10)]),
        ('Vegetable Stir Fry', [('Broccoli', 150), ('Carrots', 100), ('Bell Pepper', 100), ('Garlic', 10), ('Olive Oil', 15)]),
        ('Lentil Soup', [('Lentils', 150), ('Tomato', 200), ('Spinach', 100), ('Garlic', 5)]),
        ('Greek Salad with Feta', [('Tomato', 150), ('Spinach', 100), ('Cheddar Cheese', 50), ('Olive Oil', 15)]),
        ('Egg White Omelette', [('Eggs', 100), ('Bell Pepper', 50), ('Olive Oil', 5)]),
        ('Overnight Oats', [('Milk', 200), ('Blueberries', 50)]),
    ]
    
    for recipe_name, ingredients in recipe_ingredients:
        recipe_id = recipe_ids[recipe_name]
        for food_name, quantity in ingredients:
            c.execute("SELECT id FROM foods WHERE name = ?", (food_name,))
            food_id = c.fetchone()[0]
            c.execute("""
                INSERT INTO recipe_ingredients (recipe_id, food_id, quantity, unit)
                VALUES (?, ?, ?, ?)
            """, (recipe_id, food_id, quantity, 'g'))
    
    # Create a store cupboard (pantry) for available ingredients
    pantry_items = [
        ('Chicken Breast', 500, 'protein'),
        ('Eggs', 12, 'protein'),
        ('Broccoli', 300, 'vegetable'),
        ('Spinach', 200, 'vegetable'),
        ('Olive Oil', 500, 'oil'),
        ('Garlic', 100, 'condiment'),
        ('Milk', 1000, 'dairy'),
    ]
    
    # Store cupboard in a separate table
    c.execute("""
        CREATE TABLE IF NOT EXISTS store_cupboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER NOT NULL,
            quantity_grams REAL NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (food_id) REFERENCES foods(id)
        )
    """)
    
    for food_name, quantity, category in pantry_items:
        c.execute("SELECT id FROM foods WHERE name = ?", (food_name,))
        food_id = c.fetchone()[0]
        c.execute("""
            INSERT INTO store_cupboard (food_id, quantity_grams)
            VALUES (?, ?)
        """, (food_id, quantity))
    
    # Create a meal plan for this week
    today = datetime.now()
    start_date = today - timedelta(days=today.weekday())
    
    c.execute("""
        INSERT INTO meal_plans (user_id, plan_date, notes)
        VALUES (?, ?, ?)
    """, (1, start_date.date(), 'Weekly meal plan'))
    
    meal_plan_id = c.lastrowid
    
    # Add meals to the plan
    meal_assignments = [
        (0, 'Grilled Chicken with Broccoli'),
        (1, 'Greek Salad with Feta'),
        (2, 'Overnight Oats'),
        (3, 'Salmon & Quinoa Bowl'),
        (4, 'Vegetable Stir Fry'),
        (5, 'Lentil Soup'),
        (6, 'Egg White Omelette'),
    ]
    
    for day_offset, recipe_name in meal_assignments:
        meal_date = start_date + timedelta(days=day_offset)
        recipe_id = recipe_ids[recipe_name]
        
        c.execute("""
            INSERT INTO meals (meal_plan_id, recipe_id, meal_type, meal_date)
            VALUES (?, ?, ?, ?)
        """, (meal_plan_id, recipe_id, 'dinner', meal_date))
    
    conn.commit()
    conn.close()
    print("✓ Database populated with recipes and test data!")

if __name__ == "__main__":
    populate_database()
