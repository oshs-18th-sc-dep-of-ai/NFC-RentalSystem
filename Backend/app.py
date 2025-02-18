from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS  # React와 연결
from auth import auth_bp
from profile import profile_bp
from rental import rental_bp
from rental_return import return_bp 

app = Flask(__name__)

# React와 연결 가능하게 함 프론트에서 확인!
CORS(app, supports_credentials=True)

# MySQL 설정
app.secret_key = 'test'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

# 블루프린트 등록
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(rental_bp)
app.register_blueprint(return_bp)

if __name__ == '__main__':
    app.run(debug=True)
