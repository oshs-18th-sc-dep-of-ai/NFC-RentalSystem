from app import mysql

# ✅ 1️⃣ 물품 대여 처리
def borrow_item(student_id, item_name, item_ids):
    try:
        cursor = mysql.connection.cursor()

        # 대여 가능 여부 확인
        format_strings = ','.join(['%s'] * len(item_ids))
        cursor.execute(
            f"SELECT product_id FROM Rentals WHERE product_id IN ({format_strings}) AND rental_status = 1",
            tuple(item_ids)
        )
        already_rented = {row[0] for row in cursor.fetchall()}

        borrowed_items = []
        errors = []

        for item_id in item_ids:
            if item_id in already_rented:
                errors.append(f"{item_id}번 물품은 이미 대여 중입니다.")
            else:
                # Rentals 테이블에 추가
                cursor.execute(
                    """INSERT INTO Rentals (student_id, product_id, rental_time, rental_status) 
                    VALUES (%s, %s, NOW(), 1)""",
                    (student_id, item_id)
                )

                # Products 테이블에서 해당 물품을 대여 불가능(available = 0)으로 변경
                cursor.execute(
                    """UPDATE Products SET available = 0 WHERE product_id = %s""",
                    (item_id,)
                )

                borrowed_items.append(item_id)

        mysql.connection.commit()
        cursor.close()

        if errors:
            return {"error": errors}, 400
        return {"message": f"{item_name} {borrowed_items}번 대여 성공!"}, 200

    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}, 500

# ✅ 2️⃣ 대여 상태 조회
def get_rental_status(student_id):
    try:
        cursor = mysql.connection.cursor()

        # 대여 정보 조회
        cursor.execute("""
            SELECT p.product_name, r.rental_time, r.return_time, r.rental_status, r.rental_id
            FROM Rentals r
            JOIN Products p ON r.product_id = p.product_id
            WHERE r.student_id = %s
        """, (student_id,))

        rentals = cursor.fetchall()
        cursor.close()

        # 대여 상태 데이터 가공
        rental_list = []
        for rental in rentals:
            product_name = rental[0]
            rental_start = rental[1].strftime('%Y-%m-%d %H:%M:%S') if rental[1] else "대여 정보 없음"
            rental_end = rental[2].strftime('%Y-%m-%d %H:%M:%S') if rental[2] else "반납 전"
            status = "대여 중" if rental[3] == 1 else "반납 완료"
            rental_id = rental[4]

            rental_list.append({
                "rental_id": rental_id,
                "product_name": product_name,
                "rental_start": rental_start,
                "rental_end": rental_end,
                "status": status
            })

        return {"rented_items": rental_list}

    except Exception as e:
        return {"error": str(e)}, 500
