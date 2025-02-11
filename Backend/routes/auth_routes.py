from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from services.auth_service import register_user
from config import db

# Blueprint 설정
auth_bp = Blueprint('auth', __name__)

# 로그인 API
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    student_id = data.get('student_id')
    password = data.get('password')
    
    if not student_id or not password:
        return jsonify({'error': '학번과 비밀번호를 입력해주세요.'}), 400
    
    student = db.session.execute(
        "SELECT student_id, student_name, student_password FROM Students WHERE student_id = :id",
        {'id': student_id}
    ).fetchone()
    
    if student and check_password_hash(student[2], password):
        return jsonify({'message': '로그인 성공!', 'student_id': student[0], 'student_name': student[1]})
    else:
        return jsonify({'error': '잘못된 ID 또는 비밀번호입니다.'}), 401

