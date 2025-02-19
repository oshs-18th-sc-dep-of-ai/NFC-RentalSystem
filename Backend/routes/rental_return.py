# React에서 /rental_request_return/:id를 호출하면 해당 제품의 반납 요청 (반납 대기 상태로 변경)
# 관리자가 /admin/approve_return/:id를 호출하면 최종 반납 승인 (반납 완료 상태로 변경)

from flask import Blueprint, jsonify, session
from extensions import mysql

# 블루프린트
return_bp = Blueprint('rental_return', __name__)

# 반납 요청(React에서 `/rental_request_return/:id` 호출)
@return_bp.route('/rental_request_return/<int:id>', methods=['POST'])
def request_rental_return(id):
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE Rentals SET rental_status = 2 WHERE id = %s
    """, (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "반납 요청이 완료되었습니다. 관리자의 승인을 기다려주세요.", "status": "pending"}), 200

# 관리자가 반납 승인(React에서 `/admin/approve_return/:_id` 호출)
@return_bp.route('/admin/approve_return/<int:id>', methods=['POST'])
def approve_rental_return(id):
    if 'admin_id' not in session:
        return jsonify({"message": "관리자 권한이 필요합니다.", "status": "error"}), 403

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE id = %s AND rental_status = 2
    """, (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "반납이 승인되었습니다!", "status": "success"}), 200
