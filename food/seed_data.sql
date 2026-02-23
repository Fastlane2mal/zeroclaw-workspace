-- Seed data for food database

-- Insert users
INSERT INTO users (name, dietary_restrictions, health_conditions, preferences) VALUES
('Alice', 'vegetarian', 'none', 'loves Mediterranean food'),
('Bob', 'none', 'diabetic', 'prefers low-carb meals');

-- Insert foods/ingredients
INSERT INTO foods (name, category, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g) VALUES
('Chicken Breast', 'Protein', 165, 31, 0, 3.6, 0),
('Salmon', 'Protein', 208, 20, 0, 13, 0),
('Eggs', 'Protein', 155, 13, 1.1, 11, 0),
('Greek Yogurt', 'Dairy', 59, 10, 3.3, 0.4, 0),
('Broccoli', 'Vegetables', 34, 2.8, 7, 0.4, 2.4),
('Spinach', 'Vegetables', 23, 2.7, 3.6, 0.4, 2.2),
('Carrots', 'Vegetables', 41, 0.9, 10, 0.2, 2.8),
('Bell Peppers', 'Vegetables', 31, 1, 7.3, 0.3, 2.2),
('Brown Rice', 'Grains', 112, 2.6, 24, 0.9, 1.8),
('Quinoa', 'Grains', 120, 4.4, 21, 1.9, 2.8),
('Olive Oil', 'Oils', 884, 0, 0, 100, 0),
('Garlic', 'Vegetables', 149, 6.6, 33, 0.5, 2.1),
('Lemon', 'Fruits', 29, 1.1, 9, 0.3, 2.8),
('Tomatoes', 'Vegetables', 18, 0.9, 3.9, 0.2, 1.2),
('Onions', 'Vegetables', 40, 1.1, 9, 0.1, 1.7),
('Sweet Potatoes', 'Vegetables', 86, 1.6, 20, 0.1, 3),
('Almonds', 'Nuts', 579, 21, 22, 50, 12.5),
('Blueberries', 'Fruits', 57, 0.7, 14, 0.3, 2.4),
('Avocado', 'Fruits', 160, 2, 9, 15, 7),
('Turmeric', 'Spices', 312, 10, 67, 3.2, 21);

-- Insert recipes
INSERT INTO recipes (name, description, servings, prep_time_mins, cook_time_mins, difficulty, dietary_tags) VALUES
('Grilled Salmon with Roasted Vegetables', 'Healthy salmon fillet with seasonal roasted veg', 2, 15, 25, 'easy', 'gluten-free, high-protein'),
('Vegetarian Buddha Bowl', 'Quinoa, roasted veggies, avocado and tahini dressing', 1, 20, 30, 'easy', 'vegetarian, vegan-friendly'),
('Spinach and Egg Frittata', 'Protein-packed breakfast with fresh spinach', 2, 10, 20, 'easy', 'vegetarian, gluten-free'),
('Turmeric Chicken Stir-Fry', 'Anti-inflammatory chicken with broccoli and peppers', 2, 15, 20, 'medium', 'gluten-free, high-protein'),
('Sweet Potato and Lentil Curry', 'Warming vegetarian curry with aromatic spices', 4, 20, 35, 'medium', 'vegetarian, vegan-friendly'),
('Mediterranean Quinoa Salad', 'Fresh salad with quinoa, tomatoes, peppers and lemon dressing', 2, 15, 10, 'easy', 'vegetarian, vegan-friendly'),
('Baked Chicken with Herbs', 'Simple roasted chicken breast with garlic and lemon', 2, 10, 30, 'easy', 'gluten-free, high-protein'),
('Broccoli and Almond Stir-Fry', 'Crunchy vegetable stir-fry with almonds and garlic', 2, 15, 15, 'easy', 'vegetarian, vegan-friendly');

-- Insert recipe ingredients
INSERT INTO recipe_ingredients (recipe_id, food_id, quantity, unit) VALUES
-- Grilled Salmon with Roasted Vegetables (1)
(1, 2, 200, 'g'),  -- Salmon
(1, 4, 100, 'g'),  -- Broccoli
(1, 7, 150, 'g'),  -- Carrots
(1, 8, 100, 'g'),  -- Bell Peppers
(1, 11, 15, 'ml'), -- Olive Oil
(1, 12, 2, 'cloves'), -- Garlic
(1, 13, 1, 'whole'), -- Lemon

-- Vegetarian Buddha Bowl (2)
(2, 10, 150, 'g'), -- Quinoa
(2, 5, 100, 'g'),  -- Broccoli
(2, 19, 100, 'g'), -- Avocado
(2, 15, 50, 'g'),  -- Onions
(2, 14, 100, 'g'), -- Tomatoes
(2, 11, 15, 'ml'), -- Olive Oil

-- Spinach and Egg Frittata (3)
(3, 3, 4, 'whole'), -- Eggs
(3, 6, 150, 'g'),   -- Spinach
(3, 15, 50, 'g'),   -- Onions
(3, 11, 10, 'ml'),  -- Olive Oil

-- Turmeric Chicken Stir-Fry (4)
(4, 1, 250, 'g'),  -- Chicken Breast
(4, 5, 150, 'g'),  -- Broccoli
(4, 8, 100, 'g'),  -- Bell Peppers
(4, 12, 3, 'cloves'), -- Garlic
(4, 20, 1, 'tsp'), -- Turmeric
(4, 11, 15, 'ml'), -- Olive Oil

-- Sweet Potato and Lentil Curry (5)
(5, 16, 300, 'g'), -- Sweet Potatoes
(5, 12, 4, 'cloves'), -- Garlic
(5, 15, 100, 'g'), -- Onions
(5, 11, 20, 'ml'), -- Olive Oil

-- Mediterranean Quinoa Salad (6)
(6, 10, 150, 'g'), -- Quinoa
(6, 14, 150, 'g'), -- Tomatoes
(6, 8, 100, 'g'),  -- Bell Peppers
(6, 11, 15, 'ml'), -- Olive Oil
(6, 13, 1, 'whole'), -- Lemon

-- Baked Chicken with Herbs (7)
(7, 1, 250, 'g'),  -- Chicken Breast
(7, 12, 3, 'cloves'), -- Garlic
(7, 13, 1, 'whole'), -- Lemon
(7, 11, 10, 'ml'), -- Olive Oil

-- Broccoli and Almond Stir-Fry (8)
(8, 5, 250, 'g'),  -- Broccoli
(8, 17, 50, 'g'),  -- Almonds
(8, 12, 3, 'cloves'), -- Garlic
(8, 11, 15, 'ml'); -- Olive Oil

-- Populate store cupboard with some initial inventory
INSERT INTO store_cupboard (food_id, quantity, unit) VALUES
(1, 500, 'g'),   -- Chicken Breast
(2, 400, 'g'),   -- Salmon
(3, 12, 'whole'), -- Eggs
(4, 500, 'ml'),  -- Greek Yogurt
(5, 600, 'g'),   -- Broccoli
(6, 300, 'g'),   -- Spinach
(7, 500, 'g'),   -- Carrots
(8, 400, 'g'),   -- Bell Peppers
(9, 1000, 'g'),  -- Brown Rice
(10, 500, 'g'),  -- Quinoa
(11, 500, 'ml'), -- Olive Oil
(12, 100, 'g'),  -- Garlic
(13, 6, 'whole'), -- Lemon
(14, 600, 'g'),  -- Tomatoes
(15, 400, 'g'),  -- Onions
(16, 800, 'g'),  -- Sweet Potatoes
(17, 300, 'g'),  -- Almonds
(18, 250, 'g'),  -- Blueberries
(19, 200, 'g'),  -- Avocado
(20, 50, 'g');   -- Turmeric

-- Insert a sample meal plan for this week
INSERT INTO meal_plans (user_id, week_start_date, week_end_date) VALUES
(1, date('now', 'start of week'), date('now', '+6 days'));

-- Insert sample meals for the week
INSERT INTO meals (meal_plan_id, day_of_week, meal_type, recipe_id) VALUES
-- Monday
(1, 'Monday', 'Breakfast', 3),    -- Spinach and Egg Frittata
(1, 'Monday', 'Lunch', 6),        -- Mediterranean Quinoa Salad
(1, 'Monday', 'Dinner', 4),       -- Turmeric Chicken Stir-Fry

-- Tuesday
(1, 'Tuesday', 'Breakfast', 3),   -- Spinach and Egg Frittata
(1, 'Tuesday', 'Lunch', 2),       -- Vegetarian Buddha Bowl
(1, 'Tuesday', 'Dinner', 1),      -- Grilled Salmon with Roasted Vegetables

-- Wednesday
(1, 'Wednesday', 'Breakfast', 3), -- Spinach and Egg Frittata
(1, 'Wednesday', 'Lunch', 6),     -- Mediterranean Quinoa Salad
(1, 'Wednesday', 'Dinner', 7),    -- Baked Chicken with Herbs

-- Thursday
(1, 'Thursday', 'Breakfast', 3),  -- Spinach and Egg Frittata
(1, 'Thursday', 'Lunch', 2),      -- Vegetarian Buddha Bowl
(1, 'Thursday', 'Dinner', 4),     -- Turmeric Chicken Stir-Fry

-- Friday
(1, 'Friday', 'Breakfast', 3),    -- Spinach and Egg Frittata
(1, 'Friday', 'Lunch', 6),        -- Mediterranean Quinoa Salad
(1, 'Friday', 'Dinner', 1),       -- Grilled Salmon with Roasted Vegetables

-- Saturday
(1, 'Saturday', 'Breakfast', 3),  -- Spinach and Egg Frittata
(1, 'Saturday', 'Lunch', 2),      -- Vegetarian Buddha Bowl
(1, 'Saturday', 'Dinner', 5),     -- Sweet Potato and Lentil Curry

-- Sunday
(1, 'Sunday', 'Breakfast', 3),    -- Spinach and Egg Frittata
(1, 'Sunday', 'Lunch', 6),        -- Mediterranean Quinoa Salad
(1, 'Sunday', 'Dinner', 8);       -- Broccoli and Almond Stir-Fry
