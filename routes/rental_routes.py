from flask import Blueprint, request, jsonify, session
from services.rental_services import borrow_item, get_rental_status

rental_bp = Blueprint('rental', __name__)

#대여 요청 API
@rental_bp.route('/borrow', methods=['POST'])
def borrow():
    data = request.json
    student_id = data.get("student_id")
    item_name = data.get("item_name")
    item_ids = data.get("item_ids")

    if not student_id or not item_name or not item_ids:
        return jsonify({'error': '대여할 학생 ID, 아이템 이름, 물품 ID가 필요합니다.'}), 400

    print(f"🔹 {student_id} 학생이 '{item_name}'(아이템 ID: {item_ids})을 대여 요청함.")

    result, status_code = borrow_item(student_id, item_name, item_ids)

    # ✅ 응답 메시지에 item_name과 item_ids 포함하여 반환
    if status_code == 200:
        result["message"] = f"{item_name} {item_ids}번 대여 성공!"

    return jsonify(result), status_code

# ✅ 2️⃣ 대여 상태 조회 API
@rental_bp.route('/status', methods=['GET'])
def rental_status():
    if 'session_student_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    student_id = session['session_student_id']
    result = get_rental_status(student_id)
    return jsonify(result)
