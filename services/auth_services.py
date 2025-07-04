from flask import session
from werkzeug.security import check_password_hash
from app import mysql

# 사용자 로그인
def login_user(student_id, password):
    cursor = mysql.connection.cursor()
    
    # 학생 정보 조회
    cursor.execute("SELECT student_id, student_name, student_password FROM Students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()

    # 평문 비밀번호 비교
    if not student or student[2] != password:
        return {"error": "잘못된 ID 또는 비밀번호입니다."}, 401

    # 세션 저장
    session['session_student_id'] = student[0]
    session['session_student_name'] = student[1]

    return {"message": "로그인 성공!", "student_id": student[0], "student_name": student[1]}, 200

def logout_user():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    return {"message": "로그아웃 되었습니다."}
