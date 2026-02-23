#!/usr/bin/env python3
"""
Handle @pantry commands from Telegram
Parses: @pantry add <items>, @pantry remove <items>, @pantry list
"""
import sqlite3
import re
from datetime import datetime

DB_PATH = "food/food.db"

class PantryHandler:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def parse_command(self, message):
        """Parse @pantry commands from message"""
        pattern = r'@pantry\s+(add|remove|list)(?:\s+(.+))?'
        match = re.search(pattern, message, re.IGNORECASE)
        
        if not match:
            return None
        
        action = match.group(1).lower()
        items_str = match.group(2)
        
        return {
            'action': action,
            'items': items_str
        }
    
    def add_items(self, items_str):
        """
        Add items to pantry: 'milk 1000g, eggs 12, chicken 500'
        Format: name quantity[unit], name quantity[unit], ...
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        items = [item.strip() for item in items_str.split(',')]
        results = []
        
        for item in items:
            # Parse "name quantity[unit]"
            parts = item.rsplit(' ', 1)
            if len(parts) == 2:
                name, qty_str = parts
                name = name.strip()
                
                # Extract number from quantity (handle g, ml, etc.)
                qty_match = re.match(r'(\d+(?:\.\d+)?)', qty_str)
                if qty_match:
                    quantity = float(qty_match.group(1))
                    
                    # Check if food exists
                    c.execute("SELECT id FROM foods WHERE name LIKE ?", (f"%{name}%",))
                    food = c.fetchone()
                    
                    if food:
                        food_id = food[0]
                        # Check if already in pantry
                        c.execute("SELECT id, quantity_grams FROM store_cupboard WHERE food_id = ?", (food_id,))
                        existing = c.fetchone()
                        
                        if existing:
                            # Update quantity
                            new_qty = existing[1] + quantity
                            c.execute("UPDATE store_cupboard SET quantity_grams = ?, last_updated = ? WHERE id = ?",
                                    (new_qty, datetime.now(), existing[0]))
                            results.append(f"✓ Updated {name}: +{quantity}g (total: {new_qty}g)")
                        else:
                            # Add new item
                            c.execute("INSERT INTO store_cupboard (food_id, quantity_grams) VALUES (?, ?)",
                                    (food_id, quantity))
                            results.append(f"✓ Added {name}: {quantity}g")
                    else:
                        results.append(f"✗ Food '{name}' not found in database")
                else:
                    results.append(f"✗ Invalid quantity format: {qty_str}")
            else:
                results.append(f"✗ Invalid format: {item}")
        
        conn.commit()
        conn.close()
        
        return "\n".join(results)
    
    def remove_items(self, items_str):
        """Remove items from pantry: 'milk, eggs, chicken'"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        items = [item.strip() for item in items_str.split(',')]
        results = []
        
        for name in items:
            c.execute("SELECT id FROM foods WHERE name LIKE ?", (f"%{name}%",))
            food = c.fetchone()
            
            if food:
                food_id = food[0]
                c.execute("DELETE FROM store_cupboard WHERE food_id = ?", (food_id,))
                results.append(f"✓ Removed {name}")
            else:
                results.append(f"✗ Food '{name}' not found")
        
        conn.commit()
        conn.close()
        
        return "\n".join(results)
    
    def list_pantry(self):
        """List all items in pantry"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT f.name, f.category, sc.quantity_grams
            FROM store_cupboard sc
            JOIN foods f ON sc.food_id = f.id
            ORDER BY f.category, f.name
        """)
        
        items = c.fetchall()
        conn.close()
        
        if not items:
            return "📦 Store cupboard is empty"
        
        # Group by category
        by_category = {}
        for name, category, qty in items:
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((name, qty))
        
        result = "📦 **Store Cupboard:**\n"
        for category in sorted(by_category.keys()):
            result += f"\n*{category.capitalize()}:*\n"
            for name, qty in sorted(by_category[category]):
                result += f"  • {name}: {qty}g\n"
        
        return result
    
    def handle_message(self, message):
        """Main handler: parse and execute command"""
        cmd = self.parse_command(message)
        
        if not cmd:
            return None
        
        action = cmd['action']
        
        if action == 'list':
            return self.list_pantry()
        elif action == 'add':
            if not cmd['items']:
                return "❌ Add what? Format: @pantry add milk 1000g, eggs 12"
            return self.add_items(cmd['items'])
        elif action == 'remove':
            if not cmd['items']:
                return "❌ Remove what? Format: @pantry remove milk, eggs"
            return self.remove_items(cmd['items'])
        
        return None


# Test
if __name__ == "__main__":
    handler = PantryHandler()
    
    # Test messages
    test_messages = [
        "@pantry add milk 1000g, eggs 12, salmon 300",
        "@pantry remove milk",
        "@pantry list",
    ]
    
    for msg in test_messages:
        print(f"\n📨 {msg}")
        result = handler.handle_message(msg)
        if result:
            print(result)
