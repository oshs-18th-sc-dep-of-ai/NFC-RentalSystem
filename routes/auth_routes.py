from flask import Blueprint, request, jsonify, redirect, url_for, flash

# Blueprint 설정
auth_bp = Blueprint('auth', __name__)

# 로그인 API
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    student_id = data.get('student_id')
    student_password = data.get('password')

    if not student_id or not student_password:
        return jsonify({'error': '학번과 비밀번호를 입력해주세요.'}), 400

    response, status_code = login_user(student_id, student_password)
    return jsonify(response), status_code

# 로그아웃 API
@auth_bp.route('/logout', methods=['GET'])
def logout():
    response = logout_user()
    flash(response["message"], "success")
    return redirect(url_for('auth.login'))
from services.auth_services import login_user, logout_user
