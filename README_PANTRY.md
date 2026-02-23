# 🍽️ @PANTRY SYSTEM - COMPLETE SETUP

**Status:** ✅ **ALL 4 COMPONENTS READY**

This Telegram-based pantry management system is fully implemented and ready to use. All messages go directly to your Telegram channel.

---

## 📋 What You Have

### ✅ 1. Database Schema
- **File:** `food/schema.sql`
- **Database:** `food/food.db` (SQLite)
- Complete schema with 8 tables for foods, recipes, meals, and shopping lists
- Ready to use immediately

### ✅ 2. @pantry Command Handler  
- **File:** `food/pantry_handler.py`
- **Commands:** `@pantry list`, `@pantry add`, `@pantry remove`
- Fuzzy matching, quantity tracking, category display
- Tested and working

### ✅ 3. Frank's Meal Planner
- **File:** `food/frank_planner.py`
- Generates 7-day meal plans from available pantry items
- Calculates shopping lists
- Formats for Telegram
- Tested and working

### ✅ 4. Telegram Integration
- **Files:** `food/telegram_pantry_bot.py`, `food/frank_scheduler.py`
- Scheduled for **Sunday 3:30 PM UTC**
- Needs configuration: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
- Ready to schedule

---

## 🚀 Quick Start (5 Minutes)

### 1. Get Credentials
```
Bot Token: Telegram @BotFather → /newbot
Channel ID: Forward message to @userinfobot
```

### 2. Configure .env
```bash
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here
```

### 3. Initialize
```bash
python3 food/setup_pantry.py
python3 food/populate_db.py
```

### 4. Schedule Frank's Update
```bash
schedule --action "create" \
  --expression "30 15 * * 0" \
  --command "cd /var/home/mal/.zeroclaw/workspace && python3 food/frank_scheduler.py"
```

### 5. Test
Send in Telegram: `@pantry list`

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **PANTRY_STATUS.txt** | Visual status overview |
| **QUICK_START.md** | 5-minute setup guide |
| **PANTRY_SETUP.md** | Complete detailed guide |
| **PANTRY_COMPLETE.md** | Full reference & features |
| **README_PANTRY.md** | This file |

---

## 💬 Usage Examples

**Add items:**
```
@pantry add milk 1000g, eggs 12, salmon 300g
```

**Check inventory:**
```
@pantry list
```

**Remove items:**
```
@pantry remove milk
```

**Automatic (Sunday 3:30 PM):**
Frank generates and posts weekly meal plan + shopping list

---

## 📁 File Structure

```
workspace/
├── README_PANTRY.md              ← START HERE
├── PANTRY_STATUS.txt             ← Visual overview
├── QUICK_START.md                ← 5-min setup
├── PANTRY_SETUP.md               ← Detailed guide
├── PANTRY_COMPLETE.md            ← Full reference
│
└── food/
    ├── food.db                   ← SQLite database
    ├── schema.sql                ← Database schema
    ├── pantry_handler.py         ← @pantry commands
    ├── frank_planner.py          ← Meal planner
    ├── frank_scheduler.py        ← Scheduler wrapper
    ├── telegram_pantry_bot.py    ← Telegram integration
    ├── setup_pantry.py           ← Setup verification
    ├── populate_db.py            ← Database seeding
    └── QUICK_START.md            ← Quick reference
```

---

## ✨ Key Features

- ✅ **Database-backed** inventory tracking
- ✅ **Fuzzy food matching** (typo-tolerant)
- ✅ **Automatic quantity aggregation**
- ✅ **Recipe management** system
- ✅ **AI meal planning** from available items
- ✅ **Shopping list generation**
- ✅ **Telegram integration** (all messages in channel)
- ✅ **Scheduled updates** (Sunday 3:30 PM)
- ✅ **Nutritional tracking** (calories, protein, etc.)

---

## 🔧 Testing Commands

```bash
# Verify setup
python3 food/setup_pantry.py

# Test @pantry handler
python3 food/pantry_handler.py

# Test meal planner
python3 food/frank_planner.py

# Test scheduler
python3 food/frank_scheduler.py

# Check schedule
schedule --action "list"
```

---

## 🎯 Next Steps

1. ✅ Read PANTRY_STATUS.txt (visual overview)
2. ✅ Follow QUICK_START.md (5-minute setup)
3. ✅ Configure .env with Telegram credentials
4. ✅ Run initialization scripts
5. ✅ Schedule Frank's update
6. ✅ Test @pantry commands in Telegram
7. ✅ Start using!

---

## 💡 Pro Tips

- **Add items when you shop** - Keep pantry accurate
- **Check @pantry list weekly** - See what's available  
- **Review Frank's plan** - Adjust if needed
- **Remove used items** - Keeps tracking accurate
- **Add custom recipes** - Customize meal suggestions

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Food not found" | Run `python3 food/populate_db.py` |
| Messages not sending | Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID |
| Cron not running | Verify with `schedule --action "list"` |
| Database errors | Delete `food.db` and rerun `setup_pantry.py` |

---

## 📖 Full Documentation

- **PANTRY_STATUS.txt** - Status overview with all details
- **QUICK_START.md** - Fastest way to get started
- **PANTRY_SETUP.md** - Complete step-by-step guide
- **PANTRY_COMPLETE.md** - Full feature reference

---

**System Status: ✅ READY**

See **QUICK_START.md** to begin!
