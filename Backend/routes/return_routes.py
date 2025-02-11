# 물품 반납 api

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
    item_name = data.get('item_name')
    
    if not student_id or not item_name:
        return jsonify({'error': '학번과 반납할 물품을 입력해주세요.'}), 400
    
    result = return_item(student_id, item_name)
    return jsonify(result)

# 반납 처리 API
@return_bp.route('/return_rental/<int:rental_id>', methods=['POST'])
def process_return_rental(rental_id):
    rental = Rental.query.filter_by(id=rental_id, rental_status=True).first()
    if not rental:
        return jsonify({'error': '해당 대여 기록을 찾을 수 없습니다.'}), 400
    
    rental.rental_status = False  # 반납 완료
    rental.return_time = datetime.datetime.now()
    db.session.commit()
    
    return jsonify({"message": "반납이 완료되었습니다.", "return_time": rental.return_time.strftime('%Y-%m-%d %H:%M:%S')})
