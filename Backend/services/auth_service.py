from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql

# 사용자 등록
def register_user(student_id, name, password):
    cursor = mysql.connection.cursor()
    
    # 학번 중복 확인
    cursor.execute("SELECT student_id FROM Students WHERE student_id = %s", (student_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        return {"error": "이미 존재하는 학번입니다."}, 400

    # 비밀번호 해싱 후 데이터 삽입
    hashed_password = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO Students (student_id, student_name, student_password) VALUES (%s, %s, %s)",
        (student_id, name, hashed_password)
    )
    mysql.connection.commit()
    cursor.close()

    return {"message": "회원가입 성공!"}

# 사용자 로그인
def login_user(student_id, password):
    cursor = mysql.connection.cursor()
    
    # 학생 정보 조회
    cursor.execute("SELECT student_id, student_name, student_password FROM Students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()

    if not student or not check_password_hash(student[2], password):
        return {"error": "잘못된 ID 또는 비밀번호입니다."}, 401

    # 세션 저장
    session['session_student_id'] = student[0]
    session['session_student_name'] = student[1]

    return {"message": "로그인 성공!", "student_id": student[0], "student_name": student[1]}

# 사용자 로그아웃
def logout_user():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    return {"message": "로그아웃 되었습니다."}
