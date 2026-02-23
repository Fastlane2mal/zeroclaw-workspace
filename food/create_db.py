#!/usr/bin/env python3
import sqlite3
import os

db_path = '/var/home/mal/.zeroclaw/workspace/food/food.db'
schema_path = '/var/home/mal/.zeroclaw/workspace/food/schema.sql'

# Remove existing database if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Create connection and execute schema
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(schema_path, 'r') as f:
    schema = f.read()
    cursor.executescript(schema)

conn.commit()
conn.close()

print(f"✓ Database created successfully at {db_path}")
