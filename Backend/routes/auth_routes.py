from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from app import mysql  

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
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT student_id, student_name, student_password FROM Students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    
    if student and check_password_hash(student[2], password):
        session['session_student_id'] = student[0]  # 학번 저장
        session['session_student_name'] = student[1]  # 이름 저장
        return jsonify({'message': '로그인 성공!', 'student_id': student[0], 'student_name': student[1]})
    else:
        return jsonify({'error': '잘못된 ID 또는 비밀번호입니다.'}), 401

# 로그아웃 API
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    flash("로그아웃 되었습니다.", "success")
    return redirect(url_for('auth.login'))
