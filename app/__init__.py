from flask import Flask, render_template
from app.config import Config
from app.routes.account_routes import account_bp
from app.routes.upload_routes import upload_bp

def create_app():
    """
    Flaskアプリケーションを作成し、設定を行います。
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # アカウント管理用のBlueprintを登録
    app.register_blueprint(account_bp, url_prefix='/account')

    # アップロード用のBlueprintを登録
    app.register_blueprint(upload_bp, url_prefix='/upload')

    # ルートURLのルーティングを追加
    @app.route('/')
    def index():
        return render_template('home.html')

    return app