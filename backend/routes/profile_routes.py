import traceback
from datetime import timedelta
from flask import Blueprint, jsonify, session, url_for, request
from extensions import mysql

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
        cursor = mysql.connection.cursor()

        # ✅ 학생 정보 조회
        cursor.execute("""
            SELECT student_id, student_name, grade, class, number
            FROM Students WHERE student_id = %s
        """, (student_id,))
        student = cursor.fetchone()

        if not student:
            cursor.close()
            return jsonify({
                "message": "학생 정보를 찾을 수 없습니다.",
                "status": "error"
            }), 404

        # ✅ 현재 대여 중인 물품 조회 (컬럼명 주의!)
        cursor.execute("""
            SELECT p.product_name, r.product_id, r.rental_time, r.return_time
            FROM Rentals r
            JOIN Products p ON r.product_id = p.product_id
            WHERE r.student_id = %s AND r.rental_status = 1
        """, (student_id,))
        rentals = cursor.fetchall()
        cursor.close()

        # ✅ JSON 형태로 변환
        rental_summary = {}
        for row in rentals:
            product_name = row[0]
            product_id = row[1]
            rentaltime = row[2]
            return_time = row[3]

            if product_name not in rental_summary:
                rental_summary[product_name] = []

            # ✅ 반납 예정 시간 = 대여 시간 + 2일
            expected_return_time = (
                (rentaltime + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
                if rentaltime else "반납 예정 없음"
            )

            rental_summary[product_name].append({
                "product_id": product_id,
                "return_time": return_time.strftime('%Y-%m-%d %H:%M:%S') if return_time else expected_return_time
            })

        return jsonify({
            "student": {
                "student_id": student[0],
                "student_name": student[1]
            },
            "rentals": rental_summary,
            "status": "success"
        }), 200

    except Exception as e:
        print("❌ profile 오류 발생:", traceback.format_exc())
        return jsonify({
            "message": "서버 내부 오류 발생",
            "status": "error"
        }), 500
@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    student_id = session.get('session_student_id')
    if not student_id:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"message": "새 비밀번호가 필요합니다.", "status": "error"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE Students SET student_pw = %s WHERE student_id = %s
        """, (new_password, student_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "비밀번호가 성공적으로 변경되었습니다.", "status": "success"}), 200

    except Exception as e:
        import traceback
        print("❌ 비밀번호 변경 오류:", traceback.format_exc())
        return jsonify({"message": "서버 오류", "status": "error"}), 500
