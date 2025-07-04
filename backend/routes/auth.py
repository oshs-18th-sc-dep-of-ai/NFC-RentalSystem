from flask import Blueprint, request, session, jsonify
from extensions import mysql
from routes.admin import ADMIN_ID, ADMIN_PASSWORD  # 관리자 계정

auth_bp = Blueprint('auth', __name__)

# 로그인 라우트
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    input_student_id = data.get('student_id')
    input_password = data.get('password')

    # 관리자 로그인 처리
    if input_student_id == ADMIN_ID and input_password == ADMIN_PASSWORD:
        session['admin_id'] = ADMIN_ID
        return jsonify({
            "message": "관리자 로그인 성공!",
            "status": "admin",
            "admin_id": ADMIN_ID
        }), 200

    # 학생 로그인 처리
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT student_id, student_name, student_pw FROM Students WHERE student_id = %s",
                   (input_student_id,))
    student = cursor.fetchone()
    cursor.close()

    if student and str(student[2]) == str(input_password):
        session['session_student_id'] = student[0]
        session['session_student_name'] = student[1]
        return jsonify({
            "message": "로그인 성공!",
            "status": "student",
            "student_id": student[0],
            "student_name": student[1]
        }), 200
    else:
        return jsonify({
            "message": "잘못된 ID 또는 비밀번호입니다.",
            "status": "error"
        }), 401

# 로그아웃
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "로그아웃 되었습니다."})

# 세션 확인
@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    return jsonify({
        "admin_id": session.get("admin_id"),
        "student_id": session.get("session_student_id"),
        "student_name": session.get("session_student_name")
    }), 200
