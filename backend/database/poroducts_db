CREATE DATABASE IF NOT EXISTS student24;
USE student24;

--  물품 테이블 (Products)
CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY, 
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,  --  
    available BOOLEAN DEFAULT TRUE,  -- 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
