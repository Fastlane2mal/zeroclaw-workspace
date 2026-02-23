#!/usr/bin/env python3
"""
Frank's Meal Plan Scheduler
Runs every Sunday at 3:30 PM UTC
Generates meal plan and sends to Telegram
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def send_to_telegram(message):
    """Send message to Telegram channel"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not token or not channel_id:
        print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID")
        return False
    
    # Use http_request equivalent via requests
    try:
        import requests
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': channel_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Message sent to Telegram")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        return False

def main():
    """Generate and send Frank's meal plan"""
    try:
        from food.frank_planner import FrankPlanner
        
        print(f"🍽️ Frank's Meal Plan - {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n")
        
        frank = FrankPlanner()
        plan_message = frank.generate_plan()
        
        print("Generated plan:")
        print(plan_message)
        print()
        
        # Send to Telegram
        if send_to_telegram(plan_message):
            print("✅ Scheduler completed successfully")
            return 0
        else:
            print("⚠️ Plan generated but failed to send to Telegram")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
