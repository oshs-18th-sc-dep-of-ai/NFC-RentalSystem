from flask import Blueprint, request, jsonify
from services.admin_services import get_summary, add_item, delete_item, update_item_status, force_return  # import를 최상단으로 이동

admin_bp = Blueprint('admin', __name__)

# 전체 현황 요약 API
@admin_bp.route('/summary', methods=['GET'])
def summary():
    return jsonify(get_summary())

# 물품 추가 API
@admin_bp.route('/items', methods=['POST'])
def register_item():
    data = request.json
    return jsonify(add_item(data))

# 물품 삭제 API
@admin_bp.route('/items/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    return jsonify(delete_item(item_id))

# 대여 가능 여부 설정 API
@admin_bp.route('/items/<int:item_id>/status', methods=['PUT'])
def change_item_status(item_id):
    data = request.json
    return jsonify(update_item_status(item_id, data.get('status')))

# 강제 반납 APIA
@admin_bp.route('/return/<int:rental_id>', methods=['PUT'])
def admin_return_item(rental_id):
    return jsonify(force_return(rental_id))
