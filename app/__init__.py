from flask import Flask
from app.config import Config
from app.routes.account_routes import account_bp
from app.routes.routes import main  # この行を修正

def create_app():
    """
    Flaskアプリケーションを作成し、設定を行います。
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # アカウント管理用のBlueprintを登録
    app.register_blueprint(account_bp, url_prefix='/account')

    # メインのBlueprintを登録
    app.register_blueprint(main)  # この行を修正

    return app