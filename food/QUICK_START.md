# @pantry Quick Start (5 minutes)

## Step 1: Get Telegram Credentials

### Bot Token:
1. Open Telegram, find @BotFather
2. Send `/newbot`
3. Follow prompts, choose a name
4. Copy the token (e.g., `123456:ABC-DEF1234...`)

### Channel ID:
1. Create a Telegram channel (or use existing)
2. Add your bot to the channel (as admin)
3. Send a message in the channel
4. Forward it to @userinfobot
5. Copy the channel ID (e.g., `-100123456789`)

---

## Step 2: Configure Environment

Edit `.env` in workspace root:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here
```

---

## Step 3: Initialize Database

```bash
cd /var/home/mal/.zeroclaw/workspace
python3 food/setup_pantry.py
```

Expected output:
```
✓ Database schema created
✓ PantryHandler imported successfully
✓ FrankPlanner imported successfully
✅ Setup complete!
```

---

## Step 4: Seed Sample Data

```bash
python3 food/populate_db.py
```

This adds ~50 common ingredients and 10+ recipes.

---

## Step 5: Schedule Frank's Update

Choose one:

### Option A (Recommended):
```bash
schedule \
  --action "create" \
  --expression "30 15 * * 0" \
  --command "cd /var/home/mal/.zeroclaw/workspace && python3 food/frank_scheduler.py"
```

### Option B (Alternative):
```bash
cron_add \
  --name "frank-sunday-meal-plan" \
  --schedule '{"kind":"cron","expr":"30 15 * * 0","tz":"UTC"}' \
  --job_type "shell" \
  --command "cd /var/home/mal/.zeroclaw/workspace && python3 food/frank_scheduler.py"
```

Verify:
```bash
schedule --action "list"
# or
cron_list
```

---

## Step 6: Test Everything

### Test Database:
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('food/food.db')
c = conn.cursor()
for table in ['foods', 'recipes', 'store_cupboard']:
    c.execute(f'SELECT COUNT(*) FROM {table}')
    print(f'{table}: {c.fetchone()[0]} rows')
conn.close()
"
```

### Test @pantry Handler:
```bash
python3 food/pantry_handler.py
```

### Test Frank's Planner:
```bash
python3 food/frank_planner.py
```

---

## Step 7: Start Using It!

### In your Telegram channel:

**Add items:**
```
@pantry add milk 1000g, eggs 12, salmon 300g, spinach 200g
```

**Check inventory:**
```
@pantry list
```

**Remove items:**
```
@pantry remove milk
```

**Sunday 3:30 PM:** Frank automatically posts weekly meal plan! 🍽️

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Food not found" | Run `python3 food/populate_db.py` |
| Bot doesn't send messages | Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID |
| Cron job not running | Verify schedule with `schedule --action "list"` |
| Database errors | Delete `food/food.db` and rerun `setup_pantry.py` |

---

## Commands Reference

```bash
# Setup
python3 food/setup_pantry.py              # Verify installation
python3 food/populate_db.py               # Add sample data

# Testing
python3 food/pantry_handler.py            # Test @pantry
python3 food/frank_planner.py             # Test meal planner
python3 food/frank_scheduler.py           # Test scheduler

# Scheduling
schedule --action "create" --expression "30 15 * * 0" --command "..."
schedule --action "list"
schedule --action "get" --id <job_id>
```

---

## What's Happening

1. **@pantry commands** → Parsed by `pantry_handler.py` → Updates SQLite database
2. **Database** → Stores foods, recipes, and current inventory
3. **Frank's Planner** → Runs Sunday 3:30 PM → Reads pantry → Generates meal plan
4. **Telegram** → Sends formatted messages to your channel

---

## Next: Advanced Usage

See `PANTRY_SETUP.md` for:
- Full database schema details
- Recipe management
- Shopping list generation
- Nutritional tracking
- Custom meal plans
