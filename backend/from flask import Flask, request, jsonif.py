from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# 🔹 세션 키 설정
app.secret_key = 'test'

# 🔹 MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

# ✅ 로그인 API (JSON 응답)
@app.route('/login', methods=['POST'])
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
        session['session_student_id'] = student[0]
        session['session_student_name'] = student[1]
        return jsonify({"message": "로그인 성공!", "status": "success", "student_id": student[0], "student_name": student[1]}), 200
    else:
        return jsonify({"message": "잘못된 ID 또는 비밀번호입니다.", "status": "error"}), 401

# ✅ 로그아웃 API (JSON 응답)
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    return jsonify({"message": "로그아웃 되었습니다.", "status": "success"}), 200

# ✅ 프로필 API (대여 내역 포함)
@app.route('/profile', methods=['GET'])
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

    # 대여한 제품 조회
    cursor.execute("""
        SELECT p.product_name, r.rental_rentaltime, r.rental_returntime, r.rental_status, r.rental_id
        FROM Rentals r
        JOIN Products p ON r.product_id = p.product_id
        WHERE r.student_id = %s
    """, (session['session_student_id'],))
    rentals = cursor.fetchall()
    cursor.close()

    # JSON 변환
    rental_records = [
        {
            "product_name": rental[0],
            "rental_time": rental[1].strftime('%Y-%m-%d %H:%M:%S') if rental[1] else None,
            "return_time": rental[2].strftime('%Y-%m-%d %H:%M:%S') if rental[2] else None,
            "status": "대여 중" if rental[3] == 1 else "반납 완료",
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

# ✅ 반납 API (JSON 응답)
@app.route('/return_rental/<int:rental_id>', methods=['POST'])
def return_rental(rental_id):
    if 'session_student_id' not in session:
        return jsonify({"message": "로그인이 필요합니다.", "status": "error"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE rental_id = %s
    """, (rental_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "반납이 완료되었습니다.", "status": "success"}), 200

# Flask 앱 실행
if __name__ == '__main__':
    app.run(debug=True)
