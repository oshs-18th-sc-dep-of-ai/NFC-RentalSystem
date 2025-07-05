CREATE DATABASE IF NOT EXISTS student24_db;
USE student24_db;

CREATE TABLE IF NOT EXISTS Rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    product_id INT NOT NULL,
    rental_rentaltime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rental_returntime DATETIME NULL,
    rental_status TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT chk_rental_status CHECK (rental_status IN (0, 1, 2, 3, 4)),
    CONSTRAINT fk_rentals_students FOREIGN KEY (student_id)
      REFERENCES Students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_rentals_products FOREIGN KEY (product_id)
      REFERENCES Products(product_id) ON DELETE CASCADE
);

-- 2410101 학생이 product_id=1 (우산 1번) 대여
INSERT INTO Rentals (student_id, product_id, rental_status)
VALUES ('2410101', 1, 1);

-- 반납 요청 (rental_status = 2)
INSERT INTO Rentals (student_id, product_id, rental_status)
VALUES ('2410101', 2, 2); 

-- 반납 완료 (rental_status = 0)
INSERT INTO Rentals (student_id, product_id, rental_status, rental_returntime)
VALUES ('2410102', 3, 0, NOW());
