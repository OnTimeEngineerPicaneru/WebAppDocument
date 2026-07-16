# ToDoアプリケーション

Flask + SQLAlchemyで構築したタスク管理Webアプリケーションです。
ユーザー認証機能を備え、個人ごとにタスクを管理できます。

## 目次

- [機能概要](#機能概要)
- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ方法](#セットアップ方法)
- [使い方](#使い方)
- [データベース構成](#データベース構成)
- [開発ガイド](#開発ガイド)
- [トラブルシューティング](#トラブルシューティング)

---

## 機能概要

### 実装済み機能

- ✅ **ユーザー認証**
  - ユーザー登録
  - ログイン/ログアウト
  - セッション管理

- ✅ **タスク管理（CRUD操作）**
  - タスクの作成（Create）
  - タスク一覧表示（Read、ログイン中のユーザー自身のタスクのみ）
  - タスクの編集（Update）
  - タスクの削除（Delete）

- ✅ **タスクステータス管理**
  - 未達成（NOT_STARTED）
  - 進行中（IN_PROGRESS）
  - 実施済み（COMPLETED）
  - 保留中（PENDING）

- ✅ **セキュリティ**
  - ログイン必須ページの保護（`@login_required`）
  - パスワードはハッシュ化して保存・照合（`werkzeug.security`）
  - 自分のタスクのみ一覧表示・編集・削除可能
  - 削除前の確認ダイアログ
  - `SECRET_KEY` は環境変数（`.env`）から読み込み

- ✅ **UI/UX**
  - Bootstrap 5による洗練されたデザイン
  - レスポンシブ対応
  - ステータスバッジによる視覚的なフィードバック
  - フラッシュメッセージによる操作結果の通知

---

## 技術スタック

### バックエンド

- **Python 3.x**
- **Flask** - Webアプリケーションフレームワーク
- **Flask-SQLAlchemy** - ORM（データベース操作）
- **Flask-Login** - ユーザー認証管理
- **Flask-Migrate** - データベースマイグレーション
- **python-dotenv** - `.env`ファイルからの環境変数読み込み

### フロントエンド

- **HTML5**
- **Bootstrap 5.3.0** - CSSフレームワーク
- **Jinja2** - テンプレートエンジン

### データベース

- **SQLite** - 軽量データベース

---

## プロジェクト構成

```
ToDoApplication/
├── ToDoApplication/              # アプリケーションディレクトリ
│   ├── app.py                    # Flaskアプリケーションのエントリーポイント
│   ├── config.py                 # 設定ファイル（DB接続、シークレットキーなど）
│   ├── models.py                 # データベースモデル（User, TaskList）
│   ├── views.py                  # ルーティングとビュー処理
│   ├── requirements.txt          # 必要なPythonパッケージ一覧
│   ├── .env.example               # 環境変数のサンプル（コピーして.envを作成）
│   ├── templates/                # HTMLテンプレート
│   │   ├── login.html            # ログイン画面
│   │   ├── register.html         # ユーザー登録画面
│   │   ├── home.html             # タスク一覧画面
│   │   ├── add_task.html         # タスク作成画面
│   │   └── edit_task.html        # タスク編集画面
│   ├── migrations/               # データベースマイグレーションファイル
│   └── ToDoApplicationDatabase.sqlite  # SQLiteデータベースファイル（実行時に自動生成）
├── BootstrapDocument.md          # Bootstrap解説ドキュメント
└── README.md                     # このファイル
```

---

## セットアップ方法

### 1. 前提条件

以下がインストールされていることを確認してください：
- Python 3.7以上
- pip（Pythonパッケージマネージャー）

### 2. 必要なパッケージのインストール

```bash
cd ToDoApplication/ToDoApplication
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、`SECRET_KEY` を自分用の値に変更してください。

```bash
cp .env.example .env
```

`SECRET_KEY` のランダムな値は、以下のコマンドで生成できます。

```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

`.env` はGitHubには公開しないでください（`.gitignore` に追加すること）。

### 4. データベースの初期化

```bash
# データベースマイグレーションの初期化（初回のみ）
flask db init

# マイグレーションファイルの生成
flask db migrate -m "Initial migration"

# データベースに反映
flask db upgrade
```

### 5. アプリケーションの起動

```bash
python app.py
```

ブラウザで以下のURLにアクセス：
```
http://127.0.0.1:5000/
```

---

## 使い方

### 1. ユーザー登録

1. ログイン画面から「ユーザー登録」リンクをクリック
2. ログインIDとパスワードを入力
3. 「登録する」ボタンをクリック

### 2. ログイン

1. ログイン画面でIDとパスワードを入力
2. 「ログインする」ボタンをクリック
3. タスク一覧画面に遷移

### 3. タスクの作成

1. タスク一覧画面で「＋ 新しいタスクを作る」ボタンをクリック
2. タスク名を入力
3. ステータスを選択（未達成、進行中、実施済み、保留中）
4. 「登録する」ボタンをクリック

### 4. タスクの編集

1. タスク一覧画面で編集したいタスクの「編集」ボタンをクリック
2. タスク名またはステータスを変更
3. 「更新する」ボタンをクリック

### 5. タスクの削除

1. タスク一覧画面で削除したいタスクの「削除」ボタンをクリック
2. 確認ダイアログで「OK」をクリック

### 6. ログアウト

1. 画面右上の「ログアウト」ボタンをクリック

---

## データベース構成

### User（ユーザーマスタ）

| カラム名 | データ型 | 説明 | 制約 |
|---------|---------|------|------|
| id | Integer | ユーザーID（主キー） | PRIMARY KEY, AUTO INCREMENT |
| login_id | String(100) | ログインID | UNIQUE, NOT NULL |
| password | String(255) | パスワード（ハッシュ化して保存） | NOT NULL |
| created_at | DateTime | アカウント作成日時（UTC） | NOT NULL, DEFAULT=現在時刻 |

### TaskList（タスクリスト）

| カラム名 | データ型 | 説明 | 制約 |
|---------|---------|------|------|
| id | Integer | タスクID（主キー） | PRIMARY KEY, AUTO INCREMENT |
| task_name | String(100) | タスク名 | NOT NULL |
| status | Enum(TaskStatus) | タスクステータス | NOT NULL |
| created_at | DateTime | 作成日時（UTC） | NOT NULL, DEFAULT=現在時刻 |
| updated_at | DateTime | 更新日時（UTC） | NOT NULL, 更新時に自動更新 |
| user_id | Integer | ユーザーID（外部キー） | FOREIGN KEY, NOT NULL, INDEX |

**制約:**
- `user_id` と `task_name` の組み合わせで一意（同じユーザーが同じ名前のタスクを複数作成不可）
- `user_id` は `User.id` への外部キー参照

**補足:** 画面には `created_at`（UTC）を日本時間（JST）に変換した `created_at_jst` プロパティ（`models.py`で定義）を表示しています。

### TaskStatus（タスクステータス Enum）

| 値 | 日本語表記 | 説明 |
|----|-----------|------|
| NOT_STARTED | 未達成 | タスクが未着手の状態 |
| IN_PROGRESS | 進行中 | タスクが進行中の状態 |
| COMPLETED | 実施済み | タスクが完了した状態 |
| PENDING | 保留中 | タスクが一時停止している状態 |

---

## 開発ガイド

### ファイル構成の詳細

#### app.py

Flaskアプリケーションのメインファイルです。

```python
# 主な役割
- Flaskインスタンスの生成
- 設定ファイルの読み込み
- データベースの初期化
- ログイン機能の設定
- ルーティング（views.py）の読み込み
```

#### config.py

アプリケーションの設定を管理します。

```python
# 主な設定項目
- DEBUG: デバッグモードのON/OFF
- SQLALCHEMY_DATABASE_URI: データベース接続文字列
- SECRET_KEY: セッション暗号化キー（.envから読み込み）
```

**注意:** 本番環境では以下を変更してください：
- `DEBUG = False` に設定
- `.env` の `SECRET_KEY` を強力なランダム文字列に変更

#### models.py

データベースのモデル（テーブル構造）を定義します。

```python
# 主なクラス
- TaskStatus(enum.Enum): タスクステータスの列挙型
- User(db.Model, UserMixin): ユーザーモデル
- TaskList(db.Model): タスクリストモデル（created_at_jstプロパティを含む）
```

#### views.py

URLルーティングとビュー処理を行います。

```python
# 主なルート
- /                    : ログイン画面
- /register            : ユーザー登録画面
- /home                : タスク一覧画面（要ログイン、自分のタスクのみ表示）
- /add_task            : タスク作成画面（要ログイン）
- /edit_task/<id>      : タスク編集画面（要ログイン、自分のタスクのみ）
- /delete_task/<id>    : タスク削除処理（要ログイン、自分のタスクのみ）
- /logout              : ログアウト処理（要ログイン）
```

### 学習ポイント: なぜ user_id でフィルタするのか

`home()` で `TaskList.query.all()` のように全件取得してしまうと、ログイン中のユーザーに関係なく**全ユーザーのタスクが一覧に表示されてしまいます**。
`delete_task`/`edit_task` では「自分のタスクか」をチェックしているのに、一覧表示だけ全件取得すると仕様が矛盾します。

一覧・編集・削除のすべてで「自分のデータだけを扱う」ことを徹底するのが、複数ユーザーが使うWebアプリの基本です。

```python
# 誤り: 全ユーザーのタスクが見えてしまう
task_list = TaskList.query.all()

# 正しい: ログイン中のユーザーのタスクだけを取得
task_list = TaskList.query.filter_by(user_id=current_user.id).all()
```

### カスタマイズ方法

#### 1. ステータスの追加

`models.py` の `TaskStatus` Enumに新しいステータスを追加：

```python
class TaskStatus(enum.Enum):
    NOT_STARTED = "未達成"
    IN_PROGRESS = "進行中"
    COMPLETED = "実施済み"
    PENDING = "保留中"
    CANCELLED = "キャンセル済み"  # 追加例
```

HTMLテンプレート（`add_task.html`, `edit_task.html`, `home.html`）にも対応するオプションを追加。

#### 2. タスクに優先度を追加

`models.py` の `TaskList` モデルにカラムを追加：

```python
class TaskList(db.Model):
    # 既存のカラム...
    priority = db.Column(db.Integer, default=0)  # 優先度を追加
```

マイグレーションを実行：
```bash
flask db migrate -m "Add priority column"
flask db upgrade
```

#### 3. デザインのカスタマイズ

Bootstrap のカラーテーマを変更：
- `bg-primary` → `bg-info`（青色 → 水色）
- `bg-success` → `bg-warning`（緑色 → 黄色）

詳細は `BootstrapDocument.md` を参照してください。

---

## トラブルシューティング

### エラー: `ModuleNotFoundError: No module named 'flask'`

**原因:** 必要なパッケージがインストールされていません。

**解決策:**
```bash
pip install -r requirements.txt
```

### エラー: `'実施済' is not among the defined enum values`

**原因:** HTMLフォームで日本語の値を直接Enumに代入しようとしています。

**解決策:** HTMLの`<select>`タグの`value`属性をEnumのメンバー名（英語）に変更してください。

```html
<!-- 誤り -->
<option value="実施済">実施済み</option>

<!-- 正しい -->
<option value="COMPLETED">実施済み</option>
```

### エラー: データベーステーブルが見つからない

**原因:** データベースのマイグレーションが実行されていません。

**解決策:**
```bash
flask db migrate -m "Initial migration"
flask db upgrade
```

### ポート5000が既に使用されている

**原因:** 別のアプリケーションがポート5000を使用しています。

**解決策:** ポート番号を変更してください。

`app.py` の最終行を変更：
```python
if __name__ == "__main__":
    app.run(port=5001)  # ポート5001に変更
```

### ログインできない

**確認項目:**
1. ユーザー登録は完了していますか？
2. ログインIDとパスワードは正しいですか？
3. データベースファイル（`ToDoApplicationDatabase.sqlite`）は存在しますか？

**解決策:**
データベースを初期化して再度ユーザー登録を行ってください。

```bash
# データベースファイルを削除
rm ToDoApplicationDatabase.sqlite

# マイグレーションをやり直す
flask db migrate -m "Reinitialize database"
flask db upgrade
```

---

## 参考資料

### 公式ドキュメント

- [Flask 公式ドキュメント](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [Bootstrap 5 公式サイト](https://getbootstrap.com/)

### プロジェクト内ドキュメント

- [BootstrapDocument.md](./BootstrapDocument.md) - Bootstrap 5の使い方解説

---

## ライセンス

このプロジェクトは教育目的で作成されたサンプルコードです。
自由に改変・利用していただいて構いません。

---

## 作成者

桃花ラボ_Webアプリ作成クラス
授業用サンプルコード

---

## 更新履歴

### v1.1.0 (2026-07-01)

- タスク一覧が全ユーザー分表示されていた不具合を修正（自分のタスクのみ表示）
- タスク名重複時にエラー画面になる不具合を修正（重複時はメッセージ表示）
- ログイン失敗時にメッセージが表示されない不具合を修正
- パスワードをハッシュ化して保存・照合するように変更
- `SECRET_KEY` を環境変数（`.env`）から読み込むように変更
- 未使用テンプレート（`sample_data.html`）を削除
- `requirements.txt` / `.env.example` を追加

### v1.0.0 (2026-01-18)

- 初版リリース
- ユーザー認証機能の実装
- タスクCRUD操作の実装
- 4種類のタスクステータス対応
- Bootstrap 5によるUI実装
- セキュリティ機能の実装
