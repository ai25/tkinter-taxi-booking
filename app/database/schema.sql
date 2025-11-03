CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone TEXT,
    session_token TEXT,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pick_up_location TEXT NOT NULL,
    drop_off_location TEXT NOT NULL,
    pick_up_time INTEGER NOT NULL,
    vehicle TEXT NOT NULL,
    message TEXT,
    fare INTEGER NOT NULL,
    payment_type TEXT NOT NULL,
    paid INTEGER NOT NULL,
    cancelled INTEGER NOT NULL DEFAULT 0,
    payment_method_id INTEGER,
    assigned_driver_id INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (payment_method_id) REFERENCES payment_method_id(id),
    FOREIGN KEY (assigned_driver_id) REFERENCES user(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS payment_method (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_name TEXT NOT NULL,
    card_number TEXT NOT NULL UNIQUE,
    exp_month INTEGER NOT NULL,
    exp_year INTEGER NOT NULL,
    security_code INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_booking_user 
    ON booking(user_id);
CREATE INDEX IF NOT EXISTS idx_booking_driver 
    ON booking(assigned_driver_id);
CREATE INDEX IF NOT EXISTS idx_booking_time 
    ON booking(pick_up_time);
