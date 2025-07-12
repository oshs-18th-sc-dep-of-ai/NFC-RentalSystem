from flask import Blueprint, jsonify, request, session, url_for
from utils.database_util import DatabaseManager

import warnings

admin_bp = Blueprint('admin', __name__)

# 관리자 로그인
@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin_id = data.get('admin_id')
    password = data.get('password')
    
    warnings.warn("DO NOT use the dedicated admin account anymore.", FutureWarning)
    
    ADMIN_ID = None
    ADMIN_PASSWORD = None

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD and False:  # 항상 실패 (의도된 동작)
                                                                       # TODO: 계정에 관리자 여부 설정
        session['admin_id'] = admin_id  
        return jsonify({"message": "관리자 로그인 성공!", "status": "success"}), 200
    else:
        return jsonify({
            "message": "관리자 계정 정보가 틀렸습니다.",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 401

# 관리자 로그아웃
@admin_bp.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_id', None)  
    return jsonify({"message": "관리자 로그아웃 완료", "status": "success"}), 200

# 물품 추가
@admin_bp.route('/admin/add_product', methods=['POST'])
def add_product():
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 권한이 필요합니다.",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 403

    data = request.get_json()
    product_name = data.get('product_name')
    category = data.get('category')
    quantity = data.get('quantity', 0)

    if not product_name or not category or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"message": "올바른 제품명, 카테고리, 수량을 입력하세요.", "status": "error"}), 400

    dbutil = DatabaseManager()
    
    existing_product = dbutil.query("SELECT quantity FROM Products WHERE product_name = %s AND category = %s", (product_name, category)).result

    if existing_product:
        new_quantity = existing_product[0] + quantity
        dbutil.query("UPDATE Products SET quantity = %s WHERE product_name = %s AND category = %s",
                       (new_quantity, product_name, category))
    else:
        dbutil.query("INSERT INTO Products (product_name, category, quantity) VALUES (%s, %s, %s)",
                       (product_name, category, quantity))

    dbutil.commit()

    return jsonify({"message": f"{product_name}({quantity}개) 추가 완료!", "status": "success"}), 201

# 물품 삭제
@admin_bp.route('/admin/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 권한이 필요합니다.",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 403

    dbutil = DatabaseManager()

    product = dbutil.query("SELECT * FROM Products WHERE product_id = %s", (product_id,)).result

    if not product:
        return jsonify({"message": "존재하지 않는 제품입니다.", "status": "error"}), 404

    dbutil.query("DELETE FROM Products WHERE product_id = %s", (product_id,))
    dbutil.commit()

    return jsonify({"message": "물품이 삭제되었습니다!", "status": "success"}), 200

# 반납 승인
@admin_bp.route('/admin/approve_return/<int:rental_id>', methods=['POST'])
def approve_rental_return(rental_id):
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 권한이 필요합니다.",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 403

    dbutil = DatabaseManager()

    dbutil.query("""
        UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() 
        WHERE rental_id = %s AND rental_status = 2
    """, (rental_id,))
    dbutil.commit()

    return jsonify({"message": "반납이 승인되었습니다!", "status": "success"}), 200
