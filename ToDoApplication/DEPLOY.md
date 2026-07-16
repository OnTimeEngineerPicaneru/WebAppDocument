# 本番デプロイ手順(Linux VPS + Gunicorn + Nginx)

このドキュメントは、授業用の`README.md`とは別に、実際にサーバへデプロイする人向けの手順です。
`.env` や本番用の秘密鍵はGitHubに公開しないでください(`.gitignore`で除外済み)。

## 1. サーバにコードを配置する

```bash
git clone <リポジトリURL> ToDoApplication
cd ToDoApplication/ToDoApplication
```

## 2. Python仮想環境の作成と依存パッケージのインストール

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt
```

## 3. 本番用 .env の配置

このリポジトリには本番用の`.env`はコミットされていません。ローカルで生成した`.env`の中身を、
scp/sftpなど安全な方法でサーバに転送し、`ToDoApplication/ToDoApplication/.env` として配置してください。

```bash
scp .env user@your-server:/path/to/ToDoApplication/ToDoApplication/.env
```

`.env` の内容(最低限必要な項目):

```
SECRET_KEY=<secrets.token_hex(32)などで生成したランダムな値>
FLASK_DEBUG=false
```

## 4. データベースの初期化

```bash
flask db upgrade
```

## 5. systemdサービスの登録(Gunicorn)

`deploy/todoapp.service` を参考に、`User`・`WorkingDirectory`・`EnvironmentFile`・`ExecStart` のパスを
実際の環境に合わせて書き換えてから配置する。

```bash
sudo cp deploy/todoapp.service /etc/systemd/system/todoapp.service
sudo systemctl daemon-reload
sudo systemctl enable --now todoapp
sudo systemctl status todoapp
```

## 6. Nginxのリバースプロキシ設定

`deploy/nginx.conf.example` を参考に、`server_name` を実際のドメインに書き換えてから配置する。

```bash
sudo cp deploy/nginx.conf.example /etc/nginx/sites-available/todoapp
sudo ln -s /etc/nginx/sites-available/todoapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 7. HTTPS化(推奨)

Let's Encrypt(certbot)などで、Nginxの設定にSSL証明書を追加することを強く推奨します。

```bash
sudo certbot --nginx -d your-domain.example.com
```

## 更新のデプロイ手順(2回目以降)

```bash
cd /path/to/ToDoApplication/ToDoApplication
git pull
source venv/bin/activate
pip install -r requirements-prod.txt
flask db upgrade
sudo systemctl restart todoapp
```

## チェックリスト

- [ ] `.env` の `SECRET_KEY` は本番用のランダムな値に変更したか(サンプル値のまま使わない)
- [ ] `.env` の `FLASK_DEBUG` は `false` になっているか
- [ ] `.env` はサーバ上にのみ存在し、Gitにコミットされていないか
- [ ] `python app.py`(開発用サーバー)ではなく、Gunicorn経由で起動しているか
- [ ] HTTPS化されているか
