-- Smart Reading Habit Tracker - Database Schema
-- Run: mysql -u root -p < database/schema.sql

CREATE DATABASE IF NOT EXISTS reading_tracker
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE reading_tracker;

CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT NOT NULL,
    title            VARCHAR(200) NOT NULL,
    author           VARCHAR(150),
    genre            VARCHAR(100),
    difficulty_level ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    total_pages      INT,
    status           ENUM('to_read', 'reading', 'completed', 'abandoned') DEFAULT 'to_read',
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reading_sessions (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT  NOT NULL,
    book_id          INT  NOT NULL,
    session_date     DATE NOT NULL,
    start_time       TIME,
    end_time         TIME,
    duration_minutes INT  NOT NULL,
    pages_read       INT  DEFAULT 0,
    mood             ENUM('focused', 'distracted', 'tired', 'energized') DEFAULT 'focused',
    notes            TEXT,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id)  ON DELETE CASCADE
);
