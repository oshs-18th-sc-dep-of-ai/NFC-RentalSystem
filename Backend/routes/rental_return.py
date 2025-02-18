# React에서 /rental_return/:id를 호출하면 해당 제품을 반납
# DB에서 rental_status를 0으로 변경하고 반납 완료 시간 저장

from flask import Blueprint, jsonify, session
from app import mysql

# 블루프린트
return_bp = Blueprint('rental_return', __name__)

# 반납 (React에서 `/rental_return/:id` 호출)
@return_bp.route('/rental_return/<int:rental_id>', methods=['POST'])
def rental_return(rental_id):
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE rental_id = %s
    """, (rental_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "반납이 완료되었습니다.", "status": "success"}), 200
