# ===================================================
# app.py - Flaskアプリケーションの本体ファイル
# ===================================================
# アプリケーションの設定、データベースの初期化、ログイン機能の設定を行う。

from flask import Flask
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# config.pyのConfigクラスの内容を一括で読み込む
app.config.from_object("config.Config")

db.init_app(app)
migrate = Migrate(app, db)  # テーブル構造の変更を管理するマイグレーションツール
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # 未ログイン時のリダイレクト先


@login_manager.user_loader
def load_user(user_id):
    """セッションに保存されたuser_idからUserオブジェクトを取得する

    Flask-Loginがログイン状態のユーザーを復元するために自動的に呼び出す。
    """
    return db.session.get(User, int(user_id))


# views.pyのルーティングを読み込む(*ですべての関数をインポート)
from views import *

if __name__ == "__main__":
    # Flaskの開発用サーバーを起動(デフォルトでhttp://127.0.0.1:5000/)
    app.run()
