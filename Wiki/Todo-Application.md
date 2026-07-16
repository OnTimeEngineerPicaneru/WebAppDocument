# Todoアプリの概要

`ToDoApplication`は、教材で扱う技術を組み合わせたFlask製の学習用アプリです。

## 機能

- ユーザー登録
- ログイン・ログアウト
- ログイン中ユーザーのタスク一覧
- タスクの登録・編集・削除
- 未達成、進行中、実施済み、保留中の状態管理
- 作成日時の日本時間表示
- Bootstrapによる画面デザイン

## セキュリティ機能

- Werkzeugによるパスワードのハッシュ化
- Flask-Loginによるログイン状態の管理
- 自分のタスクだけを表示・編集・削除する認可処理
- Flask-WTFによるCSRF対策
- ログアウトと削除処理のPOST化
- ログインID、パスワード、タスク名、ステータスの検証
- データベース制約違反時のロールバック

## おもな構成

```text
ToDoApplication/
├─ app.py                 # Flask、DB、認証、CSRFの初期化
├─ config.py              # 環境変数とDB接続設定
├─ models.py              # User、TaskList、TaskStatus
├─ views.py               # URLと処理
├─ templates/             # Jinjaテンプレート
├─ migrations/            # DBマイグレーション
├─ requirements.txt       # 開発用依存関係
└─ requirements-prod.txt  # 本番用依存関係
```

## データベース

### user_master

ユーザーのログインID、パスワードハッシュ、作成日時を保存します。

### task_table

タスク名、状態、作成日時、更新日時、所有者のユーザーIDを保存します。

同じユーザーが同じ名前のタスクを複数登録できないよう、`user_id`と`task_name`に複合ユニーク制約があります。

## URL

| URL | メソッド | 内容 |
| --- | --- | --- |
| `/` | GET / POST | ログイン |
| `/register` | GET / POST | ユーザー登録 |
| `/home` | GET | タスク一覧 |
| `/add_task` | GET / POST | タスク追加 |
| `/edit_task/<task_id>` | GET / POST | タスク編集 |
| `/delete_task/<task_id>` | POST | タスク削除 |
| `/logout` | POST | ログアウト |

## 関連ページ

- [[開発環境のセットアップ|Setup]]
- [[セキュリティ上の注意|Security]]
- [アプリのREADME](https://github.com/OnTimeEngineerPicaneru/WebAppDocument/blob/main/ToDoApplication/README.md)
