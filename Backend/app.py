from flask import Flask, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_cors import CORS

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)

# 세션 키 설정
app.secret_key = 'test'

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'  -> 실제 비밀번호
app.config['MYSQL_DB'] = 'student24_db'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

# Blueprint 라우트 등록
from routes.auth_routes import auth_bp
from routes.rental_routes import rental_bp
from routes.return_routes import return_bp
from routes.admin_routes import admin_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(rental_bp, url_prefix='/api/rental')
app.register_blueprint(return_bp, url_prefix='/api/return')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# 메인 페이지 리다이렉트 (index → 로그인 페이지)
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Flask 실행
if __name__ == '__main__':
    app.run(debug=True)
