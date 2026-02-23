#!/usr/bin/env python3
"""
Populate food.db with healthy recipes and test data
"""

import sqlite3

def populate_database():
    conn = sqlite3.connect("food/food.db")
    cursor = conn.cursor()
    
    # Clear existing data (optional - comment out to preserve)
    # cursor.execute("DELETE FROM recipe_ingredients")
    # cursor.execute("DELETE FROM recipes")
    # cursor.execute("DELETE FROM foods")
    
    # Insert foods with nutritional data
    foods = [
        # Proteins
        ("Chicken Breast", "Protein", 165, 31, 0, 3.6, 0),
        ("Salmon", "Protein", 208, 20, 0, 13, 0),
        ("Eggs", "Protein", 155, 13, 1.1, 11, 0),
        ("Greek Yogurt", "Protein", 59, 10, 3.25, 0.4, 0),
        ("Lentils", "Protein", 116, 9, 20, 0.4, 8),
        ("Tofu", "Protein", 76, 8, 1.9, 4.8, 1.2),
        
        # Vegetables
        ("Broccoli", "Vegetable", 34, 2.8, 7, 0.4, 2.4),
        ("Spinach", "Vegetable", 23, 2.9, 3.6, 0.4, 2.2),
        ("Carrots", "Vegetable", 41, 0.9, 10, 0.2, 2.8),
        ("Bell Pepper", "Vegetable", 31, 1, 7, 0.3, 2.2),
        ("Broccoli", "Vegetable", 34, 2.8, 7, 0.4, 2.4),
        ("Kale", "Vegetable", 49, 4.3, 9, 0.9, 2.4),
        ("Tomato", "Vegetable", 18, 0.9, 3.9, 0.2, 1.2),
        ("Cucumber", "Vegetable", 16, 0.8, 3.6, 0.1, 0.5),
        ("Onion", "Vegetable", 40, 1.1, 9, 0.1, 1.7),
        ("Garlic", "Vegetable", 149, 6.4, 33, 0.5, 2.1),
        
        # Grains & Carbs
        ("Brown Rice", "Grain", 111, 2.6, 23, 0.9, 1.8),
        ("Quinoa", "Grain", 120, 4.4, 21, 1.9, 2.8),
        ("Whole Wheat Bread", "Grain", 247, 9, 41, 3, 7),
        ("Oats", "Grain", 389, 17, 66, 7, 11),
        ("Sweet Potato", "Grain", 86, 1.6, 20, 0.1, 3),
        
        # Fruits
        ("Apple", "Fruit", 52, 0.3, 14, 0.2, 2.4),
        ("Banana", "Fruit", 89, 1.1, 23, 0.3, 2.6),
        ("Blueberries", "Fruit", 57, 0.7, 14, 0.3, 2.4),
        ("Strawberries", "Fruit", 32, 0.7, 7.7, 0.3, 2),
        ("Avocado", "Fruit", 160, 2, 8.6, 15, 6.7),
        
        # Dairy & Alternatives
        ("Milk", "Dairy", 61, 3.2, 4.8, 3.3, 0),
        ("Cheese", "Dairy", 402, 25, 1.3, 33, 0),
        ("Butter", "Dairy", 717, 0.9, 0.1, 81, 0),
        
        # Oils & Condiments
        ("Olive Oil", "Oil", 884, 0, 0, 100, 0),
        ("Coconut Oil", "Oil", 892, 0, 0, 100, 0),
        ("Honey", "Condiment", 304, 0.3, 82, 0, 0),
        ("Salt", "Condiment", 0, 0, 0, 0, 0),
        ("Black Pepper", "Condiment", 251, 10, 64, 3.3, 25),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO foods (name, category, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', foods)
    
    # Get food IDs for recipe creation
    cursor.execute("SELECT id, name FROM foods")
    food_map = {name: id for id, name in cursor.fetchall()}
    
    # Insert recipes
    recipes = [
        ("Grilled Chicken with Broccoli", 30, 15, 2),
        ("Salmon & Quinoa Bowl", 35, 20, 2),
        ("Vegetable Stir Fry", 20, 10, 1),
        ("Greek Salad with Feta", 15, 5, 1),
        ("Lentil Soup", 40, 30, 2),
        ("Egg White Omelette", 15, 10, 1),
        ("Sweet Potato & Spinach", 25, 15, 1),
        ("Tofu Buddha Bowl", 30, 20, 1),
        ("Chicken Salad", 15, 10, 1),
        ("Smoothie Bowl", 10, 5, 1),
    ]
    
    recipe_ids = []
    for name, prep_time, cook_time, difficulty in recipes:
        cursor.execute('''
            INSERT INTO recipes (name, prep_time_mins, cook_time_mins, difficulty)
            VALUES (?, ?, ?, ?)
        ''', (name, prep_time, cook_time, difficulty))
        recipe_ids.append(cursor.lastrowid)
    
    # Map recipe ingredients
    recipe_ingredients = [
        # Grilled Chicken with Broccoli
        (recipe_ids[0], food_map["Chicken Breast"], 200, "g"),
        (recipe_ids[0], food_map["Broccoli"], 300, "g"),
        (recipe_ids[0], food_map["Olive Oil"], 15, "ml"),
        (recipe_ids[0], food_map["Salt"], 1, "pinch"),
        
        # Salmon & Quinoa Bowl
        (recipe_ids[1], food_map["Salmon"], 150, "g"),
        (recipe_ids[1], food_map["Quinoa"], 100, "g"),
        (recipe_ids[1], food_map["Spinach"], 100, "g"),
        (recipe_ids[1], food_map["Lemon"], 1, "whole"),
        
        # Vegetable Stir Fry
        (recipe_ids[2], food_map["Bell Pepper"], 150, "g"),
        (recipe_ids[2], food_map["Broccoli"], 200, "g"),
        (recipe_ids[2], food_map["Carrots"], 100, "g"),
        (recipe_ids[2], food_map["Garlic"], 2, "cloves"),
        (recipe_ids[2], food_map["Olive Oil"], 10, "ml"),
        
        # Greek Salad
        (recipe_ids[3], food_map["Tomato"], 200, "g"),
        (recipe_ids[3], food_map["Cucumber"], 150, "g"),
        (recipe_ids[3], food_map["Cheese"], 50, "g"),
        (recipe_ids[3], food_map["Olive Oil"], 15, "ml"),
        
        # Lentil Soup
        (recipe_ids[4], food_map["Lentils"], 200, "g"),
        (recipe_ids[4], food_map["Carrots"], 150, "g"),
        (recipe_ids[4], food_map["Onion"], 100, "g"),
        (recipe_ids[4], food_map["Garlic"], 3, "cloves"),
        
        # Egg White Omelette
        (recipe_ids[5], food_map["Eggs"], 3, "whole"),
        (recipe_ids[5], food_map["Spinach"], 100, "g"),
        (recipe_ids[5], food_map["Tomato"], 50, "g"),
        
        # Sweet Potato & Spinach
        (recipe_ids[6], food_map["Sweet Potato"], 200, "g"),
        (recipe_ids[6], food_map["Spinach"], 150, "g"),
        (recipe_ids[6], food_map["Olive Oil"], 10, "ml"),
        
        # Tofu Buddha Bowl
        (recipe_ids[7], food_map["Tofu"], 200, "g"),
        (recipe_ids[7], food_map["Brown Rice"], 100, "g"),
        (recipe_ids[7], food_map["Kale"], 100, "g"),
        (recipe_ids[7], food_map["Avocado"], 50, "g"),
        
        # Chicken Salad
        (recipe_ids[8], food_map["Chicken Breast"], 150, "g"),
        (recipe_ids[8], food_map["Spinach"], 200, "g"),
        (recipe_ids[8], food_map["Strawberries"], 100, "g"),
        (recipe_ids[8], food_map["Olive Oil"], 10, "ml"),
        
        # Smoothie Bowl
        (recipe_ids[9], food_map["Banana"], 1, "whole"),
        (recipe_ids[9], food_map["Blueberries"], 100, "g"),
        (recipe_ids[9], food_map["Greek Yogurt"], 150, "g"),
        (recipe_ids[9], food_map["Honey"], 15, "ml"),
    ]
    
    cursor.executemany('''
        INSERT INTO recipe_ingredients (recipe_id, food_id, quantity, unit)
        VALUES (?, ?, ?, ?)
    ''', recipe_ingredients)
    
    # Create sample users
    users = [
        ("Alice", "Balanced diet, no dairy", None, "Vegetarian"),
        ("Bob", "High protein, low carb", None, "Omnivore"),
    ]
    
    cursor.executemany('''
        INSERT INTO users (name, dietary_restrictions, health_conditions, preferences)
        VALUES (?, ?, ?, ?)
    ''', users)
    
    conn.commit()
    conn.close()
    
    print("✓ Database populated with recipes and test data!")
    print(f"  • Added {len(foods)} food items")
    print(f"  • Added {len(recipes)} recipes")
    print(f"  • Added {len(recipe_ingredients)} recipe ingredients")
    print(f"  • Added {len(users)} test users")

if __name__ == "__main__":
    populate_database()
