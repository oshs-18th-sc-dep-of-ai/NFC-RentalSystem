# 프론트엔드에서 /rental_request_return/:id를 호출하면 해당 제품의 반납 요청 (반납 대기 상태로 변경)
# 관리자가 /admin/approve_return/:id를 호출하면 최종 반납 승인 (반납 완료 상태로 변경)

from flask import Blueprint, request, jsonify, session
from utils.database_util import DatabaseManager

# 블루프린트
rental_return_bp = Blueprint('rental_return', __name__)

RENTAL_STATUS_RENTED         = 0
RENTAL_STATUS_PENDING_RETURN = 1
RENTAL_STATUS_RETURNED       = 2

# 반납 요청(프론트엔드에서 `/rental_request_return/:id` 호출)
@rental_return_bp.route('/rental_request_return/<int:rental_id>', methods=['POST'])
def rental_request_return(rental_id):
    if 'session_student_id' not in session:
        return jsonify({
            "message": "로그인이 필요합니다.", 
            "status": "error"
        }), 401

    db = DatabaseManager()
    
    # 반납 버튼 누른 순간의 시간 기록!
    db.query(
        f"UPDATE Rentals SET return_time=NOW(), rental_status={RENTAL_STATUS_RETURNED} " + \
         "WHERE rental_id=%(rental_id)s AND student_id=%(student_id)s",
        rental_id=rental_id, 
        student_id=session["session_student_id"],)
    db.commit()
    
    return jsonify({
        "message": "반납 요청 완료!", 
        "status": "success"
    })

# 관리자가 반납 승인(프론트엔드에서 `/admin/approve_return/:_id` 호출)
@rental_return_bp.route('/admin/approve_return/<int:id>', methods=['POST'])
def approve_rental_return(id):
    if 'admin_id' not in session:
        return jsonify({"message": "관리자 권한이 필요합니다.", "status": "error"}), 403

    db = DatabaseManager()
    db.query(
        f"UPDATE Rentals SET rental_status={RENTAL_STATUS_RENTED} WHERE " + \
        f"rental_id = %(rental_id)s AND rental_status={RENTAL_STATUS_RETURNED}",
        rental_id=id)
    db.commit()

    return jsonify({
        "message": "반납이 승인되었습니다!", 
        "status": "success"
    }), 200
