# 물품 대여 api

from flask import Blueprint, request, jsonify
from services.rental_service import borrow_item, get_rental_status

rental_bp = Blueprint('rental', __name__)

# 대여 요청 API
@rental_bp.route('/borrow', methods=['POST'])
def borrow():
    data = request.json
    student_id = data.get('student_id')
    item_name = data.get('item_name')
    
    if not student_id or not item_name:
        return jsonify({'error': '학번과 대여할 물품을 입력해주세요.'}), 400
    
    result = borrow_item(student_id, item_name)
    return jsonify(result)

# 대여 상태 조회 API
@rental_bp.route('/status/<student_id>', methods=['GET'])
def rental_status(student_id):
    result = get_rental_status(student_id)
    return jsonify(result)
