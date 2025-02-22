# React에서 물품을 대여할 때, API 호출하면 해당 제품을 대여 가능
# 대여 가능한지 확인 후 가능하면 DB에 저장하고 상태 변경

from flask import Blueprint, request, jsonify, session, url_for
from extensions import mysql

# 블루프린트 
rental_bp = Blueprint('rental', __name__)

# 물품 대여 (React에서 `/rent_product/:id` 호출)
@rental_bp.route('/rent_product/<int:product_id>', methods=['POST'])
def rent_product(product_id):
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error", "redirect_url": url_for('outh.login', _external=True)}), 401

    cursor = mysql.connection.cursor()

    # 대여 가능한지 확인
    cursor.execute("""
        SELECT COUNT(*) FROM Rentals WHERE product_id = %s AND rental_status = 1
    """, (product_id,))
    is_rented = cursor.fetchone()[0]

    if is_rented:
        return jsonify({"message": "이미 대여 중인 제품입니다.", "status": "error"}), 400

    # 대여 등록
    cursor.execute("""
        INSERT INTO Rentals (student_id, product_id, rental_rentaltime, rental_status)
        VALUES (%s, %s, NOW(), 1)
    """, (session['session_student_id'], product_id))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "대여가 완료되었습니다!", "status": "success", "redirect_url": url_for('profile.profile', _external=True)}), 200
