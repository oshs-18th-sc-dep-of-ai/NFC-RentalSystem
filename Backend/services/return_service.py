from app import mysql
import datetime

# 반납 가능한 물품 조회
def get_rental_status(student_id):
    cursor = mysql.connection.cursor()
    
    cursor.execute("""
        SELECT r.id, p.product_name, r.rental_rentaltime
        FROM Rentals r
        JOIN Products p ON r.product_id = p.product_id
        WHERE r.student_id = %s AND r.rental_status = 1
    """, (student_id,))
    
    rentals = cursor.fetchall()
    cursor.close()

    rental_list = [
        {
            "id": r[0],
            "product_name": r[1],
            "rental_time": r[2].strftime('%Y-%m-%d %H:%M:%S'),
            "overdue_days": (datetime.datetime.now() - r[2]).days - 2 if (datetime.datetime.now() - r[2]).days > 2 else 0
        }
        for r in rentals
    ]

    return {"rented_items": rental_list}

# 반납 처리 서비스 로직
def return_item(student_id, item_ids):
    cursor = mysql.connection.cursor()
    updated_items = []
    errors = []

    try:
        for item_id in item_ids:
            # 반납 가능한 대여 기록 확인
            cursor.execute("""
                SELECT id FROM Rentals WHERE id = %s AND student_id = %s AND rental_status = 1
            """, (item_id, student_id))
            rental = cursor.fetchone()

            if not rental:
                errors.append(f"{item_id}번 물품의 대여 기록을 찾을 수 없습니다.")
            else:
                # 반납 처리
                cursor.execute("""
                    UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE id = %s
                """, (item_id,))
                updated_items.append(item_id)

        mysql.connection.commit()
        cursor.close()

        if errors:
            return {"error": errors}, 400
        return {"message": f"{updated_items}번 물품 반납 완료!"}

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return {"error": str(e)}, 500
