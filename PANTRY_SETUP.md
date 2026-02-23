# @pantry System Setup Guide

## Overview
Complete Telegram-based pantry management system with:
- ✅ **@pantry commands** for managing store cupboard inventory
- ✅ **Frank's meal planner** generating weekly plans on Sunday 3:30 PM
- ✅ **Database schema** with recipes, ingredients, and shopping lists
- ✅ All messages sent to your Telegram channel

---

## 1. Database Schema ✓

**Location:** `food/schema.sql`

Tables:
- `users` - User profiles with dietary restrictions
- `foods` - Ingredient database with nutritional info
- `store_cupboard` - Current inventory (quantity in grams)
- `recipes` - Meal recipes with metadata
- `recipe_ingredients` - Recipe/ingredient mapping
- `meal_plans` - Weekly meal plans
- `meals` - Individual meal entries
- `shopping_lists` - Generated shopping lists

**Status:** Schema exists and ready to use

---

## 2. @pantry Command Handler ✓

**Location:** `food/pantry_handler.py`

### Commands:

```
@pantry list              → Show all items in store cupboard
@pantry add <items>      → Add items (format: name quantity[unit])
@pantry remove <items>   → Remove items
```

### Examples:

```
@pantry add milk 1000g, eggs 12, salmon 300g
@pantry remove milk, eggs
@pantry list
```

### Features:
- Fuzzy matching for food names
- Automatic quantity aggregation
- Category-based display
- Error handling

**Status:** Handler implemented and tested

---

## 3. Frank's Meal Planner ✓

**Location:** `food/frank_planner.py`

### Features:
- Scans available pantry items
- Generates 7-day meal plan
- Calculates shopping list
- Formats for Telegram (Markdown)

### Output:
```
🍽️ Weekly Meal Plan
Generated: Saturday, February 22, 2026

**Meal Schedule:**
*Monday:*
  🌅 Breakfast: ...
  🥗 Lunch: ...
  🍽️ Dinner: ...

**🛒 Shopping List:**
*Produce:*
  ☐ Tomatoes: 500g
  ☐ Lettuce: 200g
...
```

**Status:** Planner implemented and ready

---

## 4. Telegram Integration

### Configuration Required:

Create/update `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here
```

### Getting these values:

1. **Bot Token:** Create bot with @BotFather on Telegram
   - Command: `/newbot`
   - Copy the token (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

2. **Channel ID:** 
   - Add bot to your Telegram channel
   - Send a message
   - Forward to @userinfobot to get channel ID
   - Format: `-100123456789`

**Status:** Ready for configuration

---

## 5. Scheduler Setup

### Frank's Sunday 3:30 PM Update

Two options:

#### Option A: Using cron_add (Recommended)
```bash
cron_add \
  --name "frank-sunday-meal-plan" \
  --schedule '{"kind":"cron","expr":"30 15 * * 0","tz":"UTC"}' \
  --job_type "shell" \
  --command "cd /var/home/mal/.zeroclaw/workspace && python3 food/frank_scheduler.py"
```

#### Option B: Using schedule tool
```bash
schedule \
  --action "create" \
  --expression "30 15 * * 0" \
  --command "cd /var/home/mal/.zeroclaw/workspace && python3 food/frank_scheduler.py"
```

**Status:** Ready to schedule

---

## 6. Testing

### Test Database:
```bash
cd /var/home/mal/.zeroclaw/workspace
python3 food/setup_pantry.py
```

### Test Pantry Handler:
```bash
python3 food/pantry_handler.py
```

### Test Frank's Planner:
```bash
python3 food/frank_planner.py
```

### Test Telegram Integration:
```bash
python3 food/telegram_pantry_bot.py
```

---

## 7. Usage Workflow

### Daily Usage:
1. **Add items when you shop:**
   ```
   @pantry add milk 1000g, eggs 12, chicken 500g
   ```

2. **Check what you have:**
   ```
   @pantry list
   ```

3. **Remove items when used:**
   ```
   @pantry remove milk
   ```

### Weekly Workflow:
1. **Sunday 3:30 PM:** Frank automatically generates meal plan
2. **Review:** Check suggested meals and shopping list
3. **Shop:** Buy items from shopping list
4. **Add to pantry:** Use `@pantry add` commands
5. **Repeat:** Next Sunday gets new plan

---

## 8. Database Seeding

To populate with sample recipes and foods:

```bash
cd /var/home/mal/.zeroclaw/workspace
python3 food/populate_db.py
```

This adds:
- Common ingredients
- Sample recipes
- Nutritional data

---

## 9. File Structure

```
food/
├── food.db                    # SQLite database
├── schema.sql                 # Database schema
├── pantry_handler.py          # @pantry command handler
├── frank_planner.py           # Meal plan generator
├── frank_scheduler.py         # Scheduler wrapper
├── telegram_pantry_bot.py     # Telegram integration
├── setup_pantry.py            # Setup script
├── populate_db.py             # Database seeding
└── meal_plan.md               # Current meal plan (markdown)
```

---

## 10. Next Steps

- [ ] Set TELEGRAM_BOT_TOKEN in .env
- [ ] Set TELEGRAM_CHANNEL_ID in .env
- [ ] Run `python3 food/setup_pantry.py` to verify setup
- [ ] Run `python3 food/populate_db.py` to seed sample data
- [ ] Schedule Frank's update (see Step 5)
- [ ] Test @pantry commands in Telegram channel
- [ ] Add initial pantry items

---

## Troubleshooting

### "Food not found" errors
→ Run `populate_db.py` to add sample foods

### Telegram messages not sending
→ Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in .env

### Database locked errors
→ Ensure only one process is writing to food.db at a time

### Cron job not running
→ Check system timezone matches "UTC" in schedule

---

## Support

All components are in `/var/home/mal/.zeroclaw/workspace/food/`

For questions or issues:
1. Check logs: `cron_runs --job_id <job_id>`
2. Test manually: `python3 food/frank_scheduler.py`
3. Verify database: `sqlite3 food/food.db ".tables"`
