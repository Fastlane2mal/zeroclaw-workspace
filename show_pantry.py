#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/var/home/mal/.zeroclaw/workspace/food/food.db')
c = conn.cursor()

# Get all items from store_cupboard with food names
c.execute("""
    SELECT f.name, sc.quantity, sc.unit
    FROM store_cupboard sc
    JOIN foods f ON sc.food_id = f.id
    ORDER BY f.name ASC
""")
rows = c.fetchall()

if rows:
    print("📦 Your Store Cupboard:\n")
    for name, qty, unit in rows:
        print(f"  • {name}: {qty}{unit}")
    print(f"\n✅ Total items: {len(rows)}")
else:
    print("📭 Your cupboard is empty!")

conn.close()
