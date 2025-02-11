from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)

# 세션 키 설정
app.secret_key = 'test'

# 데이터베이스 설정 (MySQL + SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/student24_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    return redirect(url_for('login'))

# Flask 실행
if __name__ == '__main__':
    app.run(debug=True)
