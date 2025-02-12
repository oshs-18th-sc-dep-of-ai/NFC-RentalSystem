from flask import Blueprint, request, jsonify, session
from app import mysql  # app.py에서 설정한 mysql 객체 가져오기
import datetime

return_bp = Blueprint('return', __name__)

# 반납 가능한 물품 조회 API
@return_bp.route('/return/status', methods=['GET'])
def get_rental_status():
    if 'session_student_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    student_id = session['session_student_id']
    cursor = mysql.connection.cursor()
    
    cursor.execute("""
        SELECT r.id, p.product_name, r.rental_rentaltime
        FROM Rentals r
        JOIN Products p ON r.product_id = p.product_id
        WHERE r.student_id = %s AND r.rental_status = 1
    """, (student_id,))

    rentals = cursor.fetchall()
    cursor.close()

    rental_list = [
        {
            "id": r[0],
            "product_name": r[1],
            "rental_time": r[2].strftime('%Y-%m-%d %H:%M:%S'),
            "overdue_days": (datetime.datetime.now() - r[2]).days - 2 if (datetime.datetime.now() - r[2]).days > 2 else 0
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

    cursor = mysql.connection.cursor()

    updated_items = []
    errors = []

    try:
        for item_id in item_ids:
            cursor.execute("""
                SELECT id FROM Rentals WHERE id = %s AND student_id = %s AND rental_status = 1
            """, (item_id, student_id))
            rental = cursor.fetchone()

            if not rental:
                errors.append(f"{item_id}번 물품의 대여 기록을 찾을 수 없습니다.")
            else:
                cursor.execute("""
                    UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE id = %s
                """, (item_id,))
                updated_items.append(item_id)

        mysql.connection.commit()
        cursor.close()

        if errors:
            return jsonify({"error": errors}), 400
        return jsonify({"message": f"{updated_items}번 물품 반납 완료!"})

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': str(e)}), 500
