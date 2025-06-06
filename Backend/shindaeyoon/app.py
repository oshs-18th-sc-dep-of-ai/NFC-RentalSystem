from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)

# 세션 키 설정
app.secret_key = 'test'

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

# 로그인 페이지 리다이렉트
@app.route('/')
def index():
    return redirect(url_for('login'))

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_student_id = request.form['student_id']
        input_password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id, student_name, student_password FROM Students WHERE student_id = %s",
                       (input_student_id,))
        student = cursor.fetchone()
        cursor.close()

        # 로그인
        if student and student[2] == input_password:
            session['session_student_id'] = student[0]  # 학번 저장
            session['session_student_name'] = student[1]  # 이름 저장
            flash("로그인 성공!", "success")
            return redirect(url_for('profile'))
        else:
            flash("잘못된 ID 또는 비밀번호입니다.", "danger")  # 오류
            return redirect(url_for('login'))

    return render_template('login.html')


# 프로필 페이지 -> 로그인 해야만 접속 ㄱㄴ
@app.route('/profile')
def profile():
    if 'session_student_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # 학생 조회
    cursor.execute(""" 
        SELECT student_id, student_name, student_grade, student_class, student_number
        FROM Students WHERE student_id = %s
    """, (session['session_student_id'],))
    student = cursor.fetchone()

    # 대여 조회
    cursor.execute("""
        SELECT p.product_name, r.rental_rentaltime, r.rental_returntime, r.rental_status, r.rental_id
        FROM Rentals r
        JOIN Products p ON r.product_id = p.product_id
        WHERE r.student_id = %s
    """, (session['session_student_id'],))
    rentals = cursor.fetchall()
    cursor.close()

    # 대여 상태
    rental_status_list = []
    for rental in rentals:
        product_name = rental[0]
        rental_time = rental[1].strftime('%Y-%m-%d %H:%M:%S') if rental[1] else "X"
        return_time = rental[2].strftime('%Y-%m-%d %H:%M:%S') if rental[2] else "X"
        status = "대여 중" if rental[3] == 1 else "반납 완료"
        rental_id = rental[4]
        rental_status_list.append((product_name, rental_time, return_time, status, rental_id))

        # 여기 변수이름이 좀 맘에 안드는데 추천받아여~

    return render_template('profile.html', student=student, rental_status=rental_status_list)


# 반납 처리
@app.route('/return_rental/<int:rental_id>', methods=['POST'])
def return_rental(rental_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE Rentals SET rental_status = 0, rental_returntime = NOW() WHERE rental_id = %s
    """, (rental_id,))
    mysql.connection.commit()
    cursor.close()
    flash("반납이 완료되었습니다.", "success")
    return redirect(url_for('profile'))


# 로그아웃
@app.route('/logout')
def logout():
    session.pop('session_student_id', None)
    session.pop('session_student_name', None)
    flash("로그아웃 되었습니다.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
