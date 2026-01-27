CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'Client' NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    registered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE TABLE tours (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(120) NOT NULL,
    city VARCHAR(120) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INTEGER NOT NULL,
    base_price NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD' NOT NULL,
    description TEXT NOT NULL,
    hotel_name VARCHAR(255) NOT NULL,
    hotel_stars SMALLINT NOT NULL,
    meal_type VARCHAR(50) NOT NULL,
    included TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Available' NOT NULL
);

CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users (id),
    tour_id BIGINT NOT NULL REFERENCES tours (id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    final_price NUMERIC(10, 2) NOT NULL,
    client_comment TEXT,
    status VARCHAR(20) DEFAULT 'Created' NOT NULL,
    manager_comment TEXT
);

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_tours_country ON tours (country);
CREATE INDEX idx_tours_city ON tours (city);
CREATE INDEX idx_bookings_user ON bookings (user_id);
CREATE INDEX idx_bookings_tour ON bookings (tour_id);
