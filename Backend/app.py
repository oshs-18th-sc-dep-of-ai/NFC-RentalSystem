from flask import Flask, session
from flask_cors import CORS
from flask_session import Session  
from extensions import mysql  

app = Flask(__name__)

# React와 세션 유지 가능하게 설정 (프론트에서 꼭 withCredentials: true 확인!)
CORS(app, supports_credentials=True)

# Flask 세션 설정 추가
app.config['SECRET_KEY'] = 'test'  # 세션 유지에 필수!
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'flask_session:'

Session(app)

#  MySQL 설정
app.config['MYSQL_HOST'] = 'localhost' # 여기 실제주소로변경하기!
app.config['MYSQL_USER'] = 'root' # 사용자 이름도 변경
app.config['MYSQL_PASSWORD'] = 'PWcaoshs#osai1818!'
app.config['MYSQL_DB'] = 'student24_db'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

#  MySQL과 Flask 연결
mysql.init_app(app)

# 순환참조 계속떠서 걍 아래로 내려버린 블루프린트트
from routes.auth import auth_bp
from routes.profile_routes import profile_bp
from routes.rental import rental_bp
from routes.rental_return import return_bp
from routes.admin import admin_bp

# 블루프린트 등록
app.register_blueprint(auth_bp)  # 로그인 & 로그아웃
app.register_blueprint(profile_bp)  # 프로필 조회
app.register_blueprint(rental_bp)  # 대여 기능
app.register_blueprint(return_bp)  # 반납 기능
app.register_blueprint(admin_bp)  # 어드민(관리자) 기능

if __name__ == '__main__':
    app.run(debug=True)
