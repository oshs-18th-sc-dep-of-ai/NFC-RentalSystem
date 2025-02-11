# 로그인 및 인증 관련 기능 
from database import db
from models import Student
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, jsonify

# 사용자 등록
def register_user(student_id, name, password):
    existing_user = Student.query.filter_by(student_id=student_id).first()
    if existing_user:
        return {"error": "이미 존재하는 학번입니다."}, 400
    
    hashed_password = generate_password_hash(password)
    new_user = Student(student_id=student_id, student_name=name, student_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return {"message": "회원가입 성공!"}

# 사용자 로그인
def login_user(student_id, password):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student or not check_password_hash(student.student_password, password):
        return {"error": "잘못된 ID 또는 비밀번호입니다."}, 401
    
    session['session_student_id'] = student.student_id
    session['session_student_name'] = student.student_name
    
    return {"message": "로그인 성공!", "student_id": student.student_id, "student_name": student.student_name}

# 사용자 로그아웃
def logout_user():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    return {"message": "로그아웃 되었습니다."}

