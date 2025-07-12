# React에서 물품을 대여할 때, API 호출하면 해당 제품을 대여 가능
# 대여 가능한지 확인 후 가능하면 DB에 저장하고 상태 변경

from flask import Blueprint, request, jsonify, session, url_for
from utils.database_util import DatabaseManager
from flask_cors import cross_origin

# 블루프린트 
rental_bp = Blueprint('rental', __name__)

# 물품 대여 (React에서 `/rent_product/:id` 호출)
@rental_bp.route('/rent_product/<int:product_id>', methods=['POST'])
def rent_product(product_id):
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error", "redirect_url": url_for('outh.login', _external=True)}), 401 # 리다이렉트 추가
    
    dbutil = DatabaseManager()

    # 대여 가능한지 확인
    is_rented = dbutil.query("""
        SELECT COUNT(*) FROM Rentals WHERE product_id = %s AND rental_status = 1
    """, (product_id,)).result
    
    if is_rented:
        return jsonify({"message": "이미 대여 중인 제품입니다.", "status": "error"}), 400

    # 대여 등록
    dbutil.query("""
        INSERT INTO Rentals (student_id, product_id, rental_rentaltime, rental_status)
        VALUES (%s, %s, NOW(), 1)
    """, (session['session_student_id'], product_id))
    dbutil.commit()

    return jsonify({"message": "대여가 완료되었습니다!", "status": "success", "redirect_url": url_for('profile.profile', _external=True)}), 200 # 리다이렉트 추가

@rental_bp.route('/rental_request', methods=['POST'])
@cross_origin(supports_credentials=True)
def rental_request():
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    data = request.get_json()
    print("받은 데이터:", data)

    product_id = data.get('product_id')
    if not product_id:
        return jsonify({"message": "제품 ID가 필요합니다.", "status": "error"}), 400

    dbutil = DatabaseManager()
    
    #  대여일은 NOW(), 반납예정일은 NOW() + INTERVAL 2 DAY
    dbutil.query(
        "INSERT INTO Rentals (student_id, product_id, rental_time, expected_return_time, rental_status) VALUES (%s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 2 DAY), 1)",
        (session['session_student_id'], product_id)
    )
    dbutil.commit()

    return jsonify({"message": "대여 완료", "status": "success"})
