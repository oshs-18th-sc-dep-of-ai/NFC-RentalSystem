CREATE DATABASE IF NOT EXISTS student24_db;
USE student24_db;

-- 학생 테이블 (Students)
CREATE TABLE IF NOT EXISTS Students (
    student_id   CHAR(7)   PRIMARY KEY,
    student_name VARCHAR(128) NOT  NULL,
    student_pw   CHAR(64)     NOT  NULL,
	is_admin     BOOLEAN   DEFAULT FALSE
);

-- 물품 테이블 (Products)
CREATE TABLE IF NOT EXISTS Products (
    product_id   INT AUTO_INCREMENT PRIMARY KEY, 
    product_name VARCHAR(64)        NOT NULL,
    category     VARCHAR(64)        NOT NULL,
    quantity     INT                NOT NULL 
                                      DEFAULT 0,
    available    BOOLEAN            DEFAULT TRUE,  -- 
    created_at   TIMESTAMP          DEFAULT CURRENT_TIMESTAMP
);

-- 대여 물품 테이블 (Rentals)
CREATE TABLE IF NOT EXISTS Rentals (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    student_id  CHAR(7)               NOT NULL,
    product_id  INT                   NOT NULL,
    rental_time DATETIME              NOT NULL 
                                        DEFAULT CURRENT_TIMESTAMP,
    return_time DATETIME              NULL,
    rented      BOOLEAN               NOT NULL 
                                        DEFAULT 1,
    CONSTRAINT   chk_rental_status   CHECK (rental_status IN (0, 1, 2, 3, 4)),
    CONSTRAINT   fk_rentals_students FOREIGN KEY (student_id)
      REFERENCES Students(student_id) ON DELETE CASCADE,
    CONSTRAINT   fk_rentals_products FOREIGN KEY (product_id)
      REFERENCES Products(product_id) ON DELETE CASCADE
);