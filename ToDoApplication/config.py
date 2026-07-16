# ===================================================
# config.py - Flaskアプリケーションの設定ファイル
# ===================================================

import os
from dotenv import load_dotenv

# .envファイル(あれば)の内容を環境変数として読み込む
# .env は .gitignore で除外し、GitHubには公開しないこと
load_dotenv()


class Config(object):
    """Flaskアプリケーションの設定クラス"""

    # デバッグモード。環境変数 FLASK_DEBUG から読み込み、未設定時は安全のためFalse。
    # 開発時は .env に FLASK_DEBUG=true を設定する。本番では必ずfalse(または未設定)にする。
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    # オブジェクトの変更追跡機能(メモリを消費するため無効化)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # データベース接続先(SQLiteファイル)
    SQLALCHEMY_DATABASE_URI = "sqlite:///ToDoApplicationDatabase.sqlite"

    # SECRET_KEY: セッションを暗号化するための秘密鍵。
    # 環境変数 SECRET_KEY から読み込む(本番環境では必ず環境変数を設定すること)。
    # 環境変数が無い場合は、開発用の簡易な値を代わりに使う。
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
