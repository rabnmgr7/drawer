-- Create the database
CREATE DATABASE IF NOT EXISTS file_storage_db;
USE file_storage_db;

-- Create the files table
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    size INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the name column for faster lookups
CREATE INDEX idx_files_name ON files (name);

-- Insert sample data
INSERT INTO files (name, size) VALUES ('example.txt', 1024), ('document.pdf', 2048);