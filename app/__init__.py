from flask import Flask
from app.config import Config

def create_app():
    """
    Flaskアプリケーションを作成し、設定を行います。
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # ルートをインポートして登録
    from app import routes
    app.register_blueprint(routes.main)

    return app