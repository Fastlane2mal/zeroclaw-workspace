#!/usr/bin/env python3
"""
Setup script: Initialize database, create @pantry handler, schedule Frank's updates
"""
import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = "food/food.db"

def init_database():
    """Initialize database schema"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='foods'")
    if c.fetchone():
        print("✓ Database already initialized")
        conn.close()
        return
    
    # Read and execute schema
    with open('food/schema.sql', 'r') as f:
        schema = f.read()
    
    c.executescript(schema)
    conn.commit()
    print("✓ Database schema created")
    
    # Check counts
    for table in ['users', 'foods', 'recipes', 'store_cupboard']:
        c.execute(f'SELECT COUNT(*) FROM {table}')
        count = c.fetchone()[0]
        print(f"  {table}: {count} rows")
    
    conn.close()

def verify_pantry_handler():
    """Verify pantry handler exists and works"""
    from pantry_handler import PantryHandler
    
    handler = PantryHandler()
    print("✓ PantryHandler imported successfully")
    
    # Test parse
    cmd = handler.parse_command("@pantry list")
    if cmd:
        print(f"✓ Command parsing works: {cmd}")
    
    return handler

def verify_frank_planner():
    """Verify Frank's planner exists"""
    from frank_planner import FrankPlanner
    
    frank = FrankPlanner()
    print("✓ FrankPlanner imported successfully")
    
    return frank

if __name__ == "__main__":
    print("🔧 Setting up @pantry system...\n")
    
    try:
        init_database()
        print()
        
        handler = verify_pantry_handler()
        print()
        
        frank = verify_frank_planner()
        print()
        
        print("✅ Setup complete!")
        print("\nNext steps:")
        print("1. Create Telegram bot integration")
        print("2. Schedule Frank's Sunday 3:30pm update")
        print("3. Test @pantry commands")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
