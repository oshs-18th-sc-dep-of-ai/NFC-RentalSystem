from flask import Blueprint, jsonify, request, session, url_for
from ..utils.database_util import DatabaseManager


admin_bp = Blueprint('admin', __name__)

RENTAL_STATUS_RENTED         = 0
RENTAL_STATUS_PENDING_RETURN = 1
RENTAL_STATUS_RETURNED       = 2

# 관리자 로그인
@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin_id = data.get('admin_id')
    password = data.get('password')
    
    db = DatabaseManager()
    
    is_admin = db.query(
        "SELECT is_admin FROM Students WHERE " + \
        "student_id=%(admin_id)s AND student_pw=SHA2(%(password)s, 256)",
        admin_id=admin_id, password=password).result

    if is_admin:
        session['admin_id'] = admin_id  
        return jsonify({
            "message": "관리자 로그인 성공!", 
            "status": "success"
        }), 200
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
    return jsonify({
        "message": "관리자 로그아웃 완료", 
        "status": "success"
    }), 200

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
        return jsonify({
            "message": "올바른 제품명, 카테고리, 수량을 입력하세요.", 
            "status": "error"
        }), 400

    db = DatabaseManager()
    
    existing_product = db.query(
        "SELECT quantity FROM Products" + \
        "WHERE product_name=%(product_name)s AND category=%(category)s", 
        product_name=product_name, category=category).result

    if existing_product:
        new_quantity = existing_product[0] + quantity
        db.query(
            "UPDATE Products SET quantity=%(quantity)s" + \
            "WHERE product_name=%(product_name)s AND category=%(category)s",
            quantity=new_quantity, 
            product_name=product_name, 
            category=category)
    else:
        db.query(
            "INSERT INTO Products (product_name, category, quantity) " + \
            "VALUES (%(product_name)s, %(category)s, %(quantity)s)",
            product_name=product_name, 
            category=category, 
            quantity=quantity)
        
    db.commit()

    return jsonify({
        "message": f"{product_name}({quantity}개) 추가 완료!", 
        "status": "success"
    }), 201

# 물품 삭제
@admin_bp.route('/admin/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 권한이 필요합니다.",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 403

    db = DatabaseManager()

    product = db.query(
        "SELECT * FROM Products " + \
        "WHERE product_id=%(product_id)s", 
        product_id=product_id).result

    if not product:
        return jsonify({
            "message": "존재하지 않는 제품입니다.", 
            "status": "error"
        }), 404

    db.query(
        "DELETE FROM Products " + \
        "WHERE product_id=%(product_id)s", 
        product_id=product_id)
    db.commit()

    return jsonify({
        "message": "물품이 삭제되었습니다!", 
        "status": "success"
    }), 200

# 반납 승인
@admin_bp.route('/admin/approve_return/<int:rental_id>', methods=['POST'])
def approve_rental_return(rental_id):
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 권한이 필요합니다.",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 403

    db = DatabaseManager()

    db.query(
        f"UPDATE Rentals SET rental_status={RENTAL_STATUS_RENTED}, rental_returntime=NOW() " + \
        f"WHERE rental_id=%(rental_id)s AND rental_status={RENTAL_STATUS_RETURNED}",
        rental_id=rental_id)
    db.commit()

    return jsonify({
        "message": "반납이 승인되었습니다!", 
        "status": "success"
    }), 200

# rental_status?
# 0, 2? 