#  React에서 로그인 후 세션을 유지할 수 있도록 session에 저장
# 로그아웃 시 session.pop()으로 세션 삭제하여 상태 유지 관리

from flask import Blueprint, request, jsonify, session, url_for
from extensions import mysql 

# 블루프린트
auth_bp = Blueprint('auth', __name__)

# 로그인 (React에서 `/login` 호출)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    input_student_id = data.get('student_id')
    input_password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT student_id, student_name, student_password FROM Students WHERE student_id = %s",
                   (input_student_id,))
    student = cursor.fetchone()
    cursor.close()

    if student and student[2] == input_password:
        # 로그인 성공 시 세션 저장 (React에서 세션 유지 됨됨)
        session['session_student_id'] = student[0]
        session['session_student_name'] = student[1]
        return jsonify({"message": "로그인 성공!", "status": "success", "student_id": student[0], "student_name": student[1], "redirect_url": url_for('profile.profile', _external=True)}), 200
    else:
        return jsonify({"message": "잘못된 ID 또는 비밀번호입니다.", "status": "error"}), 401

# 로그아웃 (React에서 `/logout` 호출)
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    return jsonify({"message": "로그아웃 되었습니다.", "status": "success", "redirect_url": url_for('outh.login', _external=True)}), 200
