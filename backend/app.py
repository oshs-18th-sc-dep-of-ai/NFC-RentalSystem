from flask                 import Flask
from flask_cors            import CORS
from flask_session         import Session
from utils.database_util   import DatabaseManager
from utils.config_util     import ConfigManager as Config

from routes.auth           import auth_bp
from routes.profile_route  import profile_bp
from routes.rental         import rental_bp
from routes.rental_return  import rental_return_bp
from routes.admin          import admin_bp

app = Flask(__name__)

# 프론트엔드와 세션 유지 가능하게 설정 (프론트엔드에서 꼭 withCredentials: true 확인!)
CORS(app, supports_credentials=True)
Config().read_file("config.json")


# Flask 세션 설정 추가
app.config['SECRET_KEY']         = Config().get()["Session"]["Key"]
app.config['SESSION_TYPE']       = Config().get()["Session"]["Type"]
app.config['SESSION_PERMANENT']  = Config().get()["Session"]["Permanent"]
app.config['SESSION_USE_SIGNER'] = Config().get()["Session"]["UseSigner"]
app.config['SESSION_KEY_PREFIX'] = Config().get()["Session"]["KeyPrefix"]

Session(app)

# 데이터베이스 연결 초기화
DatabaseManager().connect(
    host     = Config().get()["Database"]["Host"],
    username = Config().get()["Database"]["Username"],
    password = Config().get()["Database"]["Password"],
)

# 블루프린트 등록
app.register_blueprint(auth_bp)           # 로그인 & 로그아웃
app.register_blueprint(profile_bp)        # 프로필 조회
app.register_blueprint(rental_bp)         # 대여 기능
app.register_blueprint(rental_return_bp)  # 반납 기능
app.register_blueprint(admin_bp)          # 어드민(관리자) 기능

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        DatabaseManager().close()