# ===================================================
# wsgi.py - 本番環境用のWSGIエントリーポイント
# ===================================================
# Gunicornなどの本番用WSGIサーバーは、開発用の `python app.py` (app.run()) ではなく
# このファイル経由でFlaskアプリケーションを起動する。
#
# 起動例: gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

from app import app

if __name__ == "__main__":
    app.run()
