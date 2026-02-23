-- Food Database Schema with Store Cupboard

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  dietary_restrictions TEXT,
  health_conditions TEXT,
  preferences TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Foods/Ingredients table
CREATE TABLE IF NOT EXISTS foods (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  category TEXT,
  calories_per_100g REAL,
  protein_g REAL,
  carbs_g REAL,
  fat_g REAL,
  fiber_g REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Store Cupboard - Current inventory
CREATE TABLE IF NOT EXISTS store_cupboard (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  food_id INTEGER NOT NULL,
  quantity REAL,
  unit TEXT,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- Recipes table
CREATE TABLE IF NOT EXISTS recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  servings INTEGER,
  prep_time_mins INTEGER,
  cook_time_mins INTEGER,
  difficulty TEXT,
  dietary_tags TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recipe ingredients junction table
CREATE TABLE IF NOT EXISTS recipe_ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  food_id INTEGER NOT NULL,
  quantity REAL,
  unit TEXT,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id),
  FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- Meal plans
CREATE TABLE IF NOT EXISTS meal_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  week_start_date DATE,
  week_end_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Meals (individual meal entries)
CREATE TABLE IF NOT EXISTS meals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  meal_plan_id INTEGER NOT NULL,
  day_of_week TEXT NOT NULL,
  meal_type TEXT NOT NULL,
  recipe_id INTEGER NOT NULL,
  notes TEXT,
  FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id),
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

-- Shopping lists
CREATE TABLE IF NOT EXISTS shopping_lists (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  meal_plan_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id)
);

-- Shopping list items
CREATE TABLE IF NOT EXISTS shopping_list_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  shopping_list_id INTEGER NOT NULL,
  food_id INTEGER NOT NULL,
  quantity REAL,
  unit TEXT,
  purchased BOOLEAN DEFAULT 0,
  FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists(id),
  FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_recipes_name ON recipes(name);
CREATE INDEX IF NOT EXISTS idx_foods_name ON foods(name);
CREATE INDEX IF NOT EXISTS idx_foods_category ON foods(category);
CREATE INDEX IF NOT EXISTS idx_meals_plan ON meals(meal_plan_id);
CREATE INDEX IF NOT EXISTS idx_meals_day ON meals(day_of_week);
CREATE INDEX IF NOT EXISTS idx_store_cupboard_food ON store_cupboard(food_id);
CREATE INDEX IF NOT EXISTS idx_shopping_list_items_list ON shopping_list_items(shopping_list_id);
