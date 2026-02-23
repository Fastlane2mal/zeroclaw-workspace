#!/usr/bin/env python3
"""
Telegram Bot Integration for @pantry
Handles @pantry commands and Frank's scheduled updates
"""
import os
import sys
import json
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from food.pantry_handler import PantryHandler
from food.frank_planner import FrankPlanner

class TelegramPantryBot:
    """Handle Telegram messages for @pantry and send updates"""
    
    def __init__(self):
        self.pantry = PantryHandler()
        self.frank = FrankPlanner()
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    
    def handle_message(self, message_text):
        """
        Process incoming Telegram message
        Returns: (response_text, should_send_to_channel)
        """
        # Check if it's a @pantry command
        if '@pantry' in message_text:
            response = self.pantry.handle_message(message_text)
            return response, True
        
        return None, False
    
    def send_frank_update(self):
        """
        Generate and send Frank's weekly meal plan
        Called via scheduler on Sunday 3:30pm
        """
        plan_message = self.frank.generate_plan()
        return plan_message
    
    def send_to_telegram(self, message):
        """
        Send message to Telegram channel
        Uses HTTP API via http_request tool
        """
        if not self.telegram_token or not self.channel_id:
            print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID")
            return False
        
        # This will be called by the scheduling system
        # which has access to http_request
        return {
            'method': 'POST',
            'url': f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
            'data': {
                'chat_id': self.channel_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
        }
    
    def process_incoming(self, update):
        """
        Process incoming Telegram update
        Format: {"message": {"text": "..."}, "chat": {...}}
        """
        if 'message' not in update or 'text' not in update['message']:
            return None
        
        message_text = update['message']['text']
        response, should_send = self.handle_message(message_text)
        
        if response and should_send:
            return response
        
        return None


def main():
    """Test the bot"""
    print("🤖 Telegram Pantry Bot\n")
    
    bot = TelegramPantryBot()
    
    # Test @pantry command
    test_msg = "@pantry list"
    print(f"Testing: {test_msg}")
    response, should_send = bot.handle_message(test_msg)
    if response:
        print(response)
        print(f"Should send to Telegram: {should_send}\n")
    
    # Test Frank's update
    print("Testing Frank's meal plan generation:")
    frank_msg = bot.send_frank_update()
    if frank_msg:
        print(frank_msg[:500] + "..." if len(frank_msg) > 500 else frank_msg)


if __name__ == "__main__":
    main()
