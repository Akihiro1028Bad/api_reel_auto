from flask import Flask, render_template
from app.config import Config
from app.routes.account_routes import account_bp
from app.routes.upload_routes import upload_bp
from app.routes.caption_routes import caption_bp
from app.routes.schedule_routes import schedule_bp  # 新しく追加

def create_app():
    """
    Flaskアプリケーションを作成し、設定を行います。
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # 各Blueprintを登録
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(caption_bp, url_prefix='/caption')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')  # 新しく追加

    # ルートURLのルーティングを追加
    @app.route('/')
    def index():
        return render_template('home.html')

    return app