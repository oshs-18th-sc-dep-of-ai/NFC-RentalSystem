from app import mysql

# 물품 반납 처리
def return_item(student_id, rental_id):
    try:
        cursor = mysql.connection.cursor()

        # 반납할 대여 정보 조회
        cursor.execute(
            """SELECT product_id FROM Rentals WHERE rental_id = %s AND student_id = %s AND rental_status = 1""",
            (rental_id, student_id)
        )
        rental = cursor.fetchone()

        if not rental:
            return {"error": "해당 대여 내역이 없거나 이미 반납되었습니다."}, 400

        product_id = rental[0]

        # Rentals 테이블 업데이트 (반납 처리)
        cursor.execute(
            """UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE rental_id = %s""",
            (rental_id,)
        )

        # Products 테이블에서 해당 물품을 다시 대여 가능(available = 1)으로 변경
        cursor.execute(
            """UPDATE Products SET available = 1 WHERE product_id = %s""",
            (product_id,)
        )

        mysql.connection.commit()
        cursor.close()

        return {"message": f"{product_id}번 물품 반납 완료!"}, 200

    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}, 500
