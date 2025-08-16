import traceback
from datetime import timedelta
from flask import Blueprint, jsonify, session, url_for, request
from ..utils.database_util import DatabaseManager
from werkzeug.security import generate_password_hash

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def profile():
    student_id = session.get('session_student_id')

    if not student_id:
        return jsonify({
            "message": "로그인이 필요합니다.",
            "status": "error",
            "redirect_url": url_for('auth.login')
        }), 401

    try:
        db = DatabaseManager()

        # 학생 정보 조회
        student_result = db.query(
            "SELECT student_id, student_name " +
            "FROM Students WHERE student_id=%(student_id)s",
            student_id=student_id
        ).result

        if not student_result:
            return jsonify({
                "message": "학생 정보를 찾을 수 없습니다.",
                "status": "error"
            }), 404

        # 첫 번째 학생 튜플 꺼내기
        student = student_result[0]

        # 현재 대여 중인 물품 조회
        rentals = db.query(
            "SELECT p.product_name, r.rental_time, r.return_time, r.rental_status, r.id, r.product_id " +
            "FROM Rentals r " +
            "JOIN Products p ON r.product_id = p.product_id " +
            "WHERE r.student_id=%(student_id)s",
            student_id=student_id
        ).result

        rental_records = [
            {
                "product_name": rental[0],
                "rental_time":  rental[1].strftime('%Y-%m-%d %H:%M:%S') if rental[1] else None,
                "return_time":  rental[2].strftime('%Y-%m-%d %H:%M:%S') if rental[2] else None,
                "status": "대여 중" if rental[3] == 1 else "반납 대기 중" if rental[3] == 2 else "반납 완료",
                "rental_id":    rental[4],
                "product_id":   rental[5],
            } for rental in rentals
        ]

        return jsonify({
            "student": {
                "student_id":   student[0],
                "student_name": student[1],
            },
            "rentals": rental_records
        }), 200

    except Exception as e:
        print("❌ profile 오류 발생:", traceback.format_exc())
        return jsonify({
            "message": "서버 내부 오류 발생",
            "status": "error"
        }), 500
        
from werkzeug.security import generate_password_hash

@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    student_id = session.get('session_student_id')
    if not student_id:
        return jsonify({
            "message": "로그인이 필요합니다.",
            "status": "error"
        }), 401

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({
            "message": "새 비밀번호가 필요합니다.",
            "status": "error"
        }), 400

    try:
        db = DatabaseManager()
        db.query(
            "UPDATE Students SET student_pw = SHA2(%(student_pw)s, 256) WHERE student_id = %(student_id)s",
            student_pw=new_password,
            student_id=student_id
        )
        db.commit()

        return jsonify({
            "message": "비밀번호가 성공적으로 변경되었습니다.",
            "status": "success"
        }), 200

    except Exception:
        import traceback
        print("❌ 비밀번호 변경 오류:", traceback.format_exc())
        return jsonify({
            "message": "서버 오류",
            "status": "error"
        }), 500

