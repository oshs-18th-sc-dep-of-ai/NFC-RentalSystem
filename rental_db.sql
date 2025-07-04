CREATE DATABASE IF NOT EXISTS student24_db;
USE student24_db;

CREATE TABLE IF NOT EXISTS Rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    product_id INT NOT NULL,
    rental_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 대여 시간
    return_time DATETIME NULL,  -- 반납 시간 (반납 전에는 NULL)
    rental_status TINYINT NOT NULL DEFAULT 1,  -- 1: 대여 중, 0: 반납 완료
    CONSTRAINT fk_rentals_students FOREIGN KEY (student_id)
      REFERENCES Students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_rentals_products FOREIGN KEY (product_id)
      REFERENCES Products(product_id) ON DELETE CASCADE
);


-- 2410101 학생이 product_id=1 (우산 1번) 대여
INSERT INTO Rentals (student_id, product_id, rental_status)
VALUES ('2410101', 1, 1);