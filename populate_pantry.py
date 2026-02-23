#!/usr/bin/env python3
"""Populate store_cupboard with sample items"""
import sqlite3

DB_PATH = '/var/home/mal/.zeroclaw/workspace/food/food.db'

def populate_cupboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Sample items to add
    items = [
        ('Milk', 1000, 'ml'),
        ('Eggs', 12, 'count'),
        ('Chicken Breast', 500, 'g'),
        ('Salmon', 400, 'g'),
        ('Spinach', 300, 'g'),
        ('Broccoli', 400, 'g'),
        ('Brown Rice', 500, 'g'),
        ('Olive Oil', 500, 'ml'),
        ('Tomatoes', 4, 'count'),
        ('Garlic', 1, 'bulb'),
        ('Onion', 2, 'count'),
        ('Lentils', 250, 'g'),
        ('Greek Yogurt', 500, 'g'),
        ('Cheddar Cheese', 200, 'g'),
        ('Blueberries', 250, 'g'),
    ]
    
    for food_name, qty, unit in items:
        # Check if food exists
        c.execute("SELECT id FROM foods WHERE name = ?", (food_name,))
        result = c.fetchone()
        
        if result:
            food_id = result[0]
        else:
            # Create food item if it doesn't exist
            c.execute("""
                INSERT INTO foods (name, category, calories_per_100g)
                VALUES (?, 'general', 100)
            """, (food_name,))
            food_id = c.lastrowid
        
        # Add to store_cupboard
        c.execute("""
            INSERT INTO store_cupboard (food_id, quantity, unit)
            VALUES (?, ?, ?)
        """, (food_id, qty, unit))
    
    conn.commit()
    print(f"✅ Added {len(items)} items to your cupboard!")
    conn.close()

if __name__ == "__main__":
    populate_cupboard()
