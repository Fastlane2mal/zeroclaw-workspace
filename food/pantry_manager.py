#!/usr/bin/env python3
"""
Pantry Manager - Handles store cupboard updates via Telegram
Tracks ingredients with quantities and categories
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Tuple

class PantryManager:
    def __init__(self, db_path: str = "food/food.db"):
        self.db_path = db_path
        self.init_pantry_table()
    
    def init_pantry_table(self):
        """Create pantry tracking table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pantry (
                id INTEGER PRIMARY KEY,
                food_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT DEFAULT 'units',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (food_id) REFERENCES foods(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_ingredient(self, ingredient_name: str, quantity: float = 1, unit: str = "units") -> Dict:
        """Add or update ingredient in pantry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get food_id by name
            cursor.execute('SELECT id FROM foods WHERE LOWER(name) = LOWER(?)', (ingredient_name,))
            result = cursor.fetchone()
            
            if not result:
                return {"success": False, "message": f"Ingredient '{ingredient_name}' not found in database"}
            
            food_id = result[0]
            
            # Check if already in pantry
            cursor.execute('SELECT id, quantity FROM pantry WHERE food_id = ?', (food_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Update quantity
                new_quantity = existing[1] + quantity
                cursor.execute(
                    'UPDATE pantry SET quantity = ?, last_updated = CURRENT_TIMESTAMP WHERE food_id = ?',
                    (new_quantity, food_id)
                )
                message = f"✓ Updated {ingredient_name}: {new_quantity} {unit}"
            else:
                # Add new
                cursor.execute(
                    'INSERT INTO pantry (food_id, quantity, unit) VALUES (?, ?, ?)',
                    (food_id, quantity, unit)
                )
                message = f"✓ Added {ingredient_name}: {quantity} {unit}"
            
            conn.commit()
            return {"success": True, "message": message}
        
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
        finally:
            conn.close()
    
    def remove_ingredient(self, ingredient_name: str, quantity: float = None) -> Dict:
        """Remove or reduce ingredient quantity in pantry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id FROM foods WHERE LOWER(name) = LOWER(?)', (ingredient_name,))
            result = cursor.fetchone()
            
            if not result:
                return {"success": False, "message": f"Ingredient '{ingredient_name}' not found"}
            
            food_id = result[0]
            
            if quantity is None:
                # Remove completely
                cursor.execute('DELETE FROM pantry WHERE food_id = ?', (food_id,))
                message = f"✓ Removed {ingredient_name} from pantry"
            else:
                # Reduce quantity
                cursor.execute('SELECT quantity FROM pantry WHERE food_id = ?', (food_id,))
                current = cursor.fetchone()
                
                if not current:
                    return {"success": False, "message": f"{ingredient_name} not in pantry"}
                
                new_quantity = current[0] - quantity
                if new_quantity <= 0:
                    cursor.execute('DELETE FROM pantry WHERE food_id = ?', (food_id,))
                    message = f"✓ Removed {ingredient_name} (quantity depleted)"
                else:
                    cursor.execute(
                        'UPDATE pantry SET quantity = ?, last_updated = CURRENT_TIMESTAMP WHERE food_id = ?',
                        (new_quantity, food_id)
                    )
                    message = f"✓ Reduced {ingredient_name}: {new_quantity} remaining"
            
            conn.commit()
            return {"success": True, "message": message}
        
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
        finally:
            conn.close()
    
    def list_pantry(self) -> str:
        """Get formatted list of current pantry items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.name, p.quantity, p.unit, f.category
            FROM pantry p
            JOIN foods f ON p.food_id = f.id
            ORDER BY f.category, f.name
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "🥬 **Pantry is empty**"
        
        # Group by category
        pantry_dict = {}
        for name, qty, unit, category in results:
            if category not in pantry_dict:
                pantry_dict[category] = []
            pantry_dict[category].append(f"  • {name}: {qty} {unit}")
        
        output = "🥬 **Current Pantry:**\n\n"
        for category in sorted(pantry_dict.keys()):
            output += f"*{category}*\n"
            output += "\n".join(pantry_dict[category])
            output += "\n\n"
        
        return output.strip()
    
    def parse_telegram_command(self, message: str) -> Dict:
        """Parse @pantry commands from Telegram messages"""
        if not message.startswith("@pantry"):
            return {"success": False, "message": "Not a pantry command"}
        
        parts = message.split(maxsplit=1)
        if len(parts) < 2:
            return {"success": False, "message": "Usage: @pantry add/remove/list [items]"}
        
        command = parts[1].split()[0].lower()
        
        if command == "list":
            return {"success": True, "message": self.list_pantry(), "type": "list"}
        
        elif command == "add":
            items_str = " ".join(parts[1].split()[1:])
            return self._process_add_items(items_str)
        
        elif command == "remove":
            items_str = " ".join(parts[1].split()[1:])
            return self._process_remove_items(items_str)
        
        else:
            return {"success": False, "message": f"Unknown command: {command}"}
    
    def _process_add_items(self, items_str: str) -> Dict:
        """Process comma-separated items for adding"""
        items = [item.strip() for item in items_str.split(",")]
        results = []
        
        for item in items:
            # Parse "quantity unit name" or just "name"
            parts = item.split()
            if len(parts) >= 3 and parts[0].replace(".", "").isdigit():
                quantity = float(parts[0])
                unit = parts[1]
                name = " ".join(parts[2:])
            else:
                quantity = 1
                unit = "units"
                name = item
            
            result = self.add_ingredient(name, quantity, unit)
            results.append(result["message"])
        
        message = "\n".join(results)
        return {"success": True, "message": message, "type": "add"}
    
    def _process_remove_items(self, items_str: str) -> Dict:
        """Process comma-separated items for removal"""
        items = [item.strip() for item in items_str.split(",")]
        results = []
        
        for item in items:
            result = self.remove_ingredient(item)
            results.append(result["message"])
        
        message = "\n".join(results)
        return {"success": True, "message": message, "type": "remove"}


if __name__ == "__main__":
    pm = PantryManager()
    
    # Test commands
    print(pm.parse_telegram_command("@pantry add milk, eggs, 2 kg chicken breast"))
    print(pm.parse_telegram_command("@pantry list"))
    print(pm.parse_telegram_command("@pantry remove milk"))
