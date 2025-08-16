from flask import Blueprint, request, jsonify, session, url_for
from ..utils.database_util import DatabaseManager
from collections import defaultdict

product_bp = Blueprint('product', __name__, url_prefix="/product")

# ✅ 물품 등록
@product_bp.route('/register', methods=['POST'])
def register_product():
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 로그인 필요",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 401

    data = request.get_json()
    name = data.get('product_name')
    quantity = data.get('quantity')

    if not name or quantity is None:
        return jsonify({
            "message": "물품명과 수량은 필수입니다.",
            "status": "error"
        }), 400

    try:
        quantity = int(quantity)
        db = DatabaseManager()

        # 카테고리 자동 부여
        existing = db.query("SELECT DISTINCT category FROM Products").result
        existing_ids = [int(row[0]) for row in existing if str(row[0]).isdigit()]
        new_category = str(max(existing_ids, default=0) + 1)

        # 개별 유닛 등록
        for i in range(1, quantity + 1):
            numbered_name = f"{name} {i}"
            db.query(
                "INSERT INTO Products (product_name, category, quantity) "
                "VALUES (%(product_name)s, %(category)s, %(quantity)s)",
                product_name=numbered_name,
                category=new_category,
                quantity=1
            )
        db.commit()

        return jsonify({
            "message": f"{name} 등록 완료 (카테고리: {new_category})",
            "status": "success"
        }), 200

    except Exception as e:
        print("❌ DB 오류:", e)
        return jsonify({
            "message": "서버 오류",
            "status": "error"
        }), 500


# ✅ 전체 물품 리스트 반환
@product_bp.route('/list', methods=['GET'])
def list_products():
    try:
        db = DatabaseManager()
        rows = db.query("SELECT product_name, category FROM Products").result

        data = defaultdict(int)
        for name, cat in rows:
            parts = name.strip().split()
            base_name = " ".join(parts[:-1]) if len(parts) > 1 and parts[-1].isdigit() else name
            data[base_name] += 1

        return jsonify(dict(data)), 200

    except Exception as e:
        print("❌ 목록 불러오기 오류:", e)
        return jsonify({
            "message": "목록 불러오기 실패",
            "status": "error"
        }), 500


# ✅ product_id 조회
@product_bp.route('/get_product_id', methods=['POST'])
def get_product_id():
    data = request.get_json()
    product_name = data.get("product_name")

    if not product_name:
        return jsonify({
            "message": "제품 이름이 필요합니다.",
            "status": "error"
        }), 400

    try:
        db = DatabaseManager()
        result = db.query(
            "SELECT product_id FROM Products WHERE product_name = %(product_name)s",
            product_name=product_name
        ).result

        if result:
            return jsonify({
                "product_id": result[0][0],
                "status": "success"
            }), 200
        else:
            return jsonify({
                "message": "존재하지 않는 제품입니다.",
                "status": "error"
            }), 404

    except Exception as e:
        print("❌ product_id 조회 오류:", e)
        return jsonify({
            "message": "서버 오류",
            "status": "error"
        }), 500


# ✅ 물품 삭제
@product_bp.route('/delete', methods=['POST'])
def delete_product():
    if 'admin_id' not in session:
        return jsonify({
            "message": "관리자 로그인 필요",
            "status": "error",
            "redirect_url": url_for('admin.admin_login', _external=True)
        }), 401

    data = request.get_json()
    base_name = data.get("product_name")

    if not base_name:
        return jsonify({
            "message": "제품 이름이 필요합니다.",
            "status": "error"
        }), 400

    try:
        db = DatabaseManager()
        like_pattern = f"{base_name}%"
        db.query(
            "DELETE FROM Products WHERE product_name LIKE %(pattern)s",
            pattern=like_pattern
        )
        db.commit()

        return jsonify({
            "message": "삭제 완료",
            "status": "success"
        }), 200

    except Exception as e:
        print("❌ 삭제 오류:", e)
        return jsonify({
            "message": "서버 오류",
            "status": "error"
        }), 500
