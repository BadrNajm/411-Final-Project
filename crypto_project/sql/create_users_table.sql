DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    salt TEXT NOT NULL, -- Salt for password hashing
    password TEXT NOT NULL, -- SHA-256 hashed password
    totp_secret TEXT NOT NULL, -- TOTP secret for 2FA
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
