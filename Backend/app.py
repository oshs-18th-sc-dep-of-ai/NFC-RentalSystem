from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS  # React와 연결
from auth import auth_bp
from profile import profile_bp
from rental import rental_bp
from rental_return import return_bp
from admin import admin_bp 

app = Flask(__name__)

# React와 세션 유지 가능하게 설정 (프론트에서 꼭 withCredentials: true 확인!)
CORS(app, supports_credentials=True)

# MySQL 설정
app.secret_key = 'test'
app.config['MYSQL_HOST'] = 'localhost' # MySQL 서버 주소로 변경
app.config['MYSQL_USER'] = 'root' # 사용자 이름도 변경경
app.config['MYSQL_PASSWORD'] = 'PWcaoshs#osai1818 '
app.config['MYSQL_DB'] = 'student24_db'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

# 블루프린트 등록
app.register_blueprint(auth_bp)  # 로그인 & 로그아웃
app.register_blueprint(profile_bp)  # 프로필 조회
app.register_blueprint(rental_bp)  # 대여 기능
app.register_blueprint(return_bp)  # 반납 기능
app.register_blueprint(admin_bp)  # 어드민(관리자) 기능

if __name__ == '__main__':
    app.run(debug=True)
