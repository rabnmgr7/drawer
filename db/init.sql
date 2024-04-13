CREATE DATABASE file_storage_db;
USE file_storage_db;

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);