from flask import Blueprint, request, jsonify, session
from services.return_services import return_item

return_bp = Blueprint('return', __name__)

# 반납 요청 API
@return_bp.route('/return/<int:rental_id>', methods=['POST'])
def return_rental(rental_id):
    if 'session_student_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    student_id = session['session_student_id']
    result, status_code = return_item(student_id, rental_id)
    return jsonify(result), status_code
