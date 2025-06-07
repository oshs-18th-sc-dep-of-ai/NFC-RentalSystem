# React에서 /rental_request_return/:id를 호출하면 해당 제품의 반납 요청 (반납 대기 상태로 변경)
# 관리자가 /admin/approve_return/:id를 호출하면 최종 반납 승인 (반납 완료 상태로 변경)

from flask import Blueprint, request, jsonify, session
from extensions import mysql  # ← app이 아니라 extensions에서 import!

# 블루프린트
rental_return_bp = Blueprint('rental_return', __name__)

# 반납 요청(React에서 `/rental_request_return/:id` 호출)
@rental_return_bp.route('/rental_request_return/<int:rental_id>', methods=['POST'])
def rental_request_return(rental_id):
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    cursor = mysql.connection.cursor()
    # 반납 버튼 누른 순간의 시간 기록!
    cursor.execute(
        "UPDATE Rentals SET return_time = NOW(), rental_status = 2 WHERE rental_id = %s AND student_id = %s",
        (rental_id, session['session_student_id'])
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "반납 요청 완료!", "status": "success"})

# 관리자가 반납 승인(React에서 `/admin/approve_return/:_id` 호출)
@rental_return_bp.route('/admin/approve_return/<int:id>', methods=['POST'])
def approve_rental_return(id):
    if 'admin_id' not in session:
        return jsonify({"message": "관리자 권한이 필요합니다.", "status": "error"}), 403

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE Rentals SET rental_status = 0 WHERE rental_id = %s AND rental_status = 2",
        (id,)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "반납이 승인되었습니다!", "status": "success"}), 200
