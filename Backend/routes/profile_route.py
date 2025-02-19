# React에서 /profile API를 호출->  학생 정보 + 대여 목록 확인 가능!

from flask import Blueprint, jsonify, session
from extensions import mysql

# 블루프린트 
profile_bp = Blueprint('profile', __name__)

# 프로필 조회
@profile_bp.route('/profile', methods=['GET'])
def profile():
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    cursor = mysql.connection.cursor()

    # 학생 정보 조회
    cursor.execute("""
        SELECT student_id, student_name, student_grade, student_class, student_number
        FROM Students WHERE student_id = %s
    """, (session['session_student_id'],))
    student = cursor.fetchone()

    # 대여한 물품 조회
    cursor.execute("""
        SELECT p.product_name, r.rental_rentaltime, r.rental_returntime, r.rental_status, r.rental_id
        FROM Rentals r
        JOIN Products p ON r.product_id = p.product_id
        WHERE r.student_id = %s
    """, (session['session_student_id'],))
    rentals = cursor.fetchall()
    cursor.close()

    # 리액트에서 쉽게 사용할 수 있는 !!! JSON응답으로 바뀸~
    rental_records = [
        {
            "product_name": rental[0],
            "rental_time": rental[1].strftime('%Y-%m-%d %H:%M:%S') if rental[1] else None,
            "return_time": rental[2].strftime('%Y-%m-%d %H:%M:%S') if rental[2] else None,
            "status": "대여 중" if rental[3] == 1 else "반납 대기 중" if rental[3] == 2 else "반납 완료", 
            "rental_id": rental[4],
        }
        for rental in rentals
    ]

    return jsonify({
        "student": {
            "student_id": student[0],
            "student_name": student[1],
            "student_grade": student[2],
            "student_class": student[3],
            "student_number": student[4]
        },
        "rentals": rental_records,
        "status": "success"
    }), 200
