from flask import Blueprint, request, jsonify
from app import mysql  

rental_bp = Blueprint('rental', __name__)

# 대여 요청 API
@rental_bp.route('/borrow', methods=['POST'])
def borrow():
    data = request.json
    student_id = data.get('student_id')
    item_name = data.get('item_name')
    item_ids = data.get('item_ids')

    if not student_id or not item_name or not item_ids:
        return jsonify({'error': '대여할 물품을 선택해 주세요.'}), 400

    cursor = mysql.connection.cursor()

    try:
        for item_id in item_ids:
            cursor.execute("""
                INSERT INTO Rentals (student_id, product_id, rental_rentaltime, rental_status) 
                VALUES (%s, %s, NOW(), %s)
            """, (student_id, item_id, 1))  # rental_status = 1 (대여 중)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': '대여가 완료되었습니다!', 'rented_items': item_ids})

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': str(e)}), 500

# 대여 상태 조회 API
@rental_bp.route('/status/<student_id>', methods=['GET'])
def rental_status(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT r.id, p.product_name, r.rental_rentaltime, r.rental_status 
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
            "status": "대여 중" if r[3] == 1 else "반납 완료"
        }
        for r in rentals
    ]

    return jsonify({"rented_items": rental_list})
