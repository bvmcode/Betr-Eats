CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    meal_date DATE NOT NULL,
    meal_type VARCHAR(50) NOT NULL,
    meal_description TEXT NOT NULL,
    calorie_count INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE weight (
    id SERIAL PRIMARY KEY,
    weight_date date NOT NULL,
    weight_lbs FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table goals (
    id SERIAL PRIMARY KEY,
    goal_date DATE NOT NULL,
    goal_value FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table exercise (
    id SERIAL PRIMARY KEY,
    exercise_date DATE NOT NULL,
    excercise_minutes INT not null,
    exercise_description TEXT NOT NULL,
    exercise_calories_burned INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
