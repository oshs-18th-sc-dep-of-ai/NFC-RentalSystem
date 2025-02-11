# 반납 기능 API

from flask import Blueprint, request, jsonify, session
from services.return_service import return_item
from database import db
from models import Rental
import datetime

return_bp = Blueprint('return', __name__)

# 반납 가능한 물품 조회 API
@return_bp.route('/return/status', methods=['GET'])
def get_rental_status():
    if 'session_student_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    student_id = session['session_student_id']
    rentals = Rental.query.filter_by(student_id=student_id, rental_status=True).all()

    rental_list = [
        {
            "id": r.id,
            "product_name": r.product_name,
            "rental_time": r.rental_time.strftime('%Y-%m-%d %H:%M:%S'),
            "overdue_days": (datetime.datetime.now() - r.rental_time).days - 2 if (datetime.datetime.now() - r.rental_time).days > 2 else 0
        }
        for r in rentals
    ]

    return jsonify({"rented_items": rental_list})

# 반납 요청 API
@return_bp.route('/return', methods=['PUT'])
def return_rental():
    data = request.json
    student_id = data.get('student_id')
    item_ids = data.get('item_ids')  
    
    if not student_id or not item_ids:
        return jsonify({'error': '학번과 반납할 물품을 선택해주세요.'}), 400
    
    result = return_item(student_id, item_ids)
    return jsonify(result)

# 반납 처리 API
@return_bp.route('/return_rental', methods=['POST'])
def process_return_rental():
    data = request.json
    student_id = data.get('student_id')
    item_ids = data.get('item_ids')  # 변경: 여러 개의 물품 반납 지원

    if not student_id or not item_ids:
        return jsonify({'error': '반납할 물품을 선택해주세요.'}), 400

    updated_items = []
    errors = []

    for item_id in item_ids:
        rental = Rental.query.filter_by(id=item_id, student_id=student_id, rental_status=True).first()
        if not rental:
            errors.append(f"{item_id}번 물품의 대여 기록을 찾을 수 없습니다.")
        else:
            rental.rental_status = False  # 반납 완료
            rental.return_time = datetime.datetime.now()
            updated_items.append(item_id)
    
    db.session.commit()
    
    if errors:
        return jsonify({"error": errors}), 400
    return jsonify({"message": f"{updated_items}번 물품 반납 완료!"})
