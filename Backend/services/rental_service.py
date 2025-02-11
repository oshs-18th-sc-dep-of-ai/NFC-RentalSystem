from flask import jsonify
from app import mysql
import datetime

# 물품 대여 처리
def borrow_item(student_id, item_name, item_ids):
    cursor = mysql.connection.cursor()
    borrowed_items = []
    errors = []

    try:
        for item_id in item_ids:
            # 이미 대여 중인지 확인
            cursor.execute(
                "SELECT rental_id FROM Rentals WHERE product_id = %s AND rental_status = 1",
                (item_id,)
            )
            existing_rental = cursor.fetchone()

            if existing_rental:
                errors.append(f"{item_name} {item_id}번은 이미 대여 중입니다.")
            else:
                # 물품 대여 처리
                cursor.execute(
                    """INSERT INTO Rentals (student_id, product_id, rental_rentaltime, rental_status) 
                    VALUES (%s, %s, NOW(), %s)""",
                    (student_id, item_id, 1)  # rental_status = 1 (대여 중)
                )
                borrowed_items.append(item_id)

        mysql.connection.commit()
        cursor.close()

        if errors:
            return {"error": errors}, 400
        return {"message": f"{item_name} {borrowed_items}번 대여 성공!"}

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return {"error": str(e)}, 500

# 대여 상태 조회
def get_rental_status(student_id):
    cursor = mysql.connection.cursor()
    
    cursor.execute(
        """SELECT r.rental_id, p.product_name, r.rental_rentaltime
           FROM Rentals r 
           JOIN Products p ON r.product_id = p.product_id
           WHERE r.student_id = %s AND r.rental_status = 1""",
        (student_id,)
    )

    rentals = cursor.fetchall()
    cursor.close()

    rental_list = [
        {
            "id": r[0],
            "product_name": r[1],
            "rental_time": r[2].strftime('%Y-%m-%d %H:%M:%S')
        }
        for r in rentals
    ]

    return {"rented_items": rental_list}
