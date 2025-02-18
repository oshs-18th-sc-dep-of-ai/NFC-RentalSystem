from flask import Blueprint, jsonify, request, session
from extensions import mysql  

# 블루프린트
admin_bp = Blueprint('admin', __name__)

# 관리자 계정 아이거진짜중요한건데 말하고다니지마셈 이빨다뽑을거임그러면
ADMIN_ID = "caoshsadmin"
ADMIN_PASSWORD ="PWoscounil18th!"

# 관리자 로그인
@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin_id = data.get('admin_id')
    password = data.get('password')

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
        session['admin_id'] = admin_id  
        return jsonify({"message": "관리자 로그인 성공!", "status": "success"}), 200
    else:
        return jsonify({"message": "관리자 계정 정보가 틀렸습니다.", "status": "error"}), 401

# 관리자 로그아웃
@admin_bp.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_id', None)  
    return jsonify({"message": "관리자 로그아웃 완료", "status": "success"}), 200

# 물품 추가
@admin_bp.route('/admin/add_product', methods=['POST'])
def add_product():
    if 'admin_id' not in session:
        return jsonify({"message": "관리자 권한이 필요합니다.", "status": "error"}), 403

    data = request.get_json()
    product_name = data.get('product_name')
    category = data.get('category')
    quantity = data.get('quantity', 0)  

    if not product_name or not category or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"message": "올바른 제품명, 카테고리, 수량을 입력하세요.", "status": "error"}), 400

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT quantity FROM Products WHERE product_name = %s AND category = %s", (product_name, category))
    existing_product = cursor.fetchone()

    if existing_product:
        new_quantity = existing_product[0] + quantity
        cursor.execute("UPDATE Products SET quantity = %s WHERE product_name = %s AND category = %s",
                       (new_quantity, product_name, category))
    else:
        cursor.execute("INSERT INTO Products (product_name, category, quantity) VALUES (%s, %s, %s)",
                       (product_name, category, quantity))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": f"{product_name}({quantity}개) 추가 완료!", "status": "success"}), 201



# 물품 삭제
@admin_bp.route('/admin/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'admin_id' not in session:  
        return jsonify({"message": "관리자 권한이 필요합니다.", "status": "error"}), 403

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM Products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        return jsonify({"message": "존재하지 않는 제품입니다.", "status": "error"}), 404

    cursor.execute("DELETE FROM Products WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "물품이 삭제되었습니다!", "status": "success"}), 200


# 반납 승인
@admin_bp.route('/admin/approve_return/<int:rental_id>', methods=['POST'])
def approve_rental_return(rental_id):
    if 'admin_id' not in session:
        return jsonify({"message": "관리자 권한이 필요합니다.", "status": "error"}), 403

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE rental_id = %s AND rental_status = 2
    """, (rental_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "반납이 승인되었습니다!", "status": "success"}), 200
