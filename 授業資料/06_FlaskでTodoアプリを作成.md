# FlaskでTodoアプリを作成する

> Webアプリ作成講座｜配布用教材 06

この教材では、5つの元教材を1つにまとめ、Flaskの環境構築からHTTP、テンプレート、データベース、ログイン、TodoのCRUD、日時表示までを順番に学びます。

---

## 1. WebページとWebアプリ

どちらもブラウザーで利用できますが、目的の見方が少し異なります。

| 観点 | Webページ | Webアプリ |
| --- | --- | --- |
| 中心となる目的 | 情報を読む | 機能を使って作業する |
| 操作の例 | 記事を読む、リンクを開く | ログイン、検索、登録、編集 |
| データ | 同じ内容を表示することが多い | 利用者や操作に応じて変わることが多い |
| おもな技術 | HTML、CSS、JavaScript | 左記に加え、サーバー側処理やデータベース |

実際のサイトは両方の特徴を持つため、境界は明確ではありません。この教材で作るTodoアプリは、利用者がタスクを登録・編集・削除するWebアプリです。

---

## 2. Flaskとは

Flaskは、PythonでWebアプリを作るためのWebフレームワークです。URLと処理を結び付けるルーティング、HTTPリクエストの読み取り、レスポンスの作成、Jinjaテンプレートとの連携などを提供します。

「マイクロフレームワーク」のマイクロは、Flask本体が小さな中核を提供し、必要な機能を拡張機能などで追加できるという意味です。小さなアプリしか作れないという意味ではありません。

### この教材で使うもの

| 名前 | 役割 |
| --- | --- |
| Flask | Webアプリ本体 |
| Jinja | HTMLテンプレート |
| Flask-SQLAlchemy | データベース操作 |
| Flask-Migrate | データベース構造の変更管理 |
| Flask-Login | ログイン状態の管理 |
| Flask-WTF | CSRF対策 |
| Werkzeug | パスワードのハッシュ化など |
| SQLite | 学習用データベース |

Flaskは特定のMVC／MVT構成を強制しません。この教材では、役割を分ける考え方を取り入れながら、最初は理解しやすい小さな構成で作ります。

---

## 3. HTTPとCRUD

ブラウザーはHTTPリクエストを送り、Flaskは処理結果をHTTPレスポンスとして返します。

```text
ブラウザー ── HTTPリクエスト ──→ Flask
ブラウザー ←─ HTTPレスポンス ─── Flask
```

### おもなHTTPメソッド

| メソッド | おもな目的 | CRUDとの対応例 |
| --- | --- | --- |
| GET | 情報を取得する | Read |
| POST | データを送信し、処理や作成を依頼する | Create |
| PUT | リソース全体を置き換える | Update |
| PATCH | リソースの一部を変更する | Update |
| DELETE | リソースを削除する | Delete |

HTMLの標準的な`form`が直接送信できるメソッドはGETとPOSTです。この教材では、作成・更新・削除をPOSTで受け付け、URLと処理名で操作を区別します。

### GET

ページや情報の取得に使います。検索条件などはクエリ文字列に入ることがあります。

```text
/tasks?status=completed
```

GETはデータを変更しない処理に使います。削除を`<a href="...">`で実装してはいけません。リンクの先読みや誤操作で削除される危険があるためです。

### POST

フォームの入力などをリクエスト本文へ入れて送ります。

```html
<form method="post">
  <input name="task_name">
  <button type="submit">登録</button>
</form>
```

POSTの本文はURLへ表示されませんが、それだけで秘密になるわけではありません。公開環境ではHTTPSを使います。

### Post/Redirect/Get

POST処理の後にHTMLを直接返すと、再読み込み時に同じ送信を繰り返す場合があります。保存後は一覧へリダイレクトします。

```text
POSTで登録 → 保存 → 一覧URLへリダイレクト → GETで一覧表示
```

---

## 4. 開発環境を作る

この教材ではWindows PowerShellとPythonが準備済みであることを前提にします。Pythonとパッケージの対応状況は変化するため、授業で指定されたバージョンを使ってください。

### 作業フォルダー

```powershell
mkdir todo_application
cd todo_application
```

### uvを利用できるか確認

```powershell
uv --version
```

見つからない場合は、講師の指示に従ってuvをインストールします。環境によっては次の方法を使えます。

```powershell
py -m pip install uv
```

### 仮想環境を作る

```powershell
uv venv .venv --python 3.12
```

`.venv`は、このプロジェクト専用のPython環境です。プロジェクトごとに環境を分けると、パッケージのバージョン衝突を減らせます。

### 仮想環境を有効にする

PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

コマンドプロンプト：

```bat
.venv\Scripts\activate.bat
```

PowerShellの実行ポリシーにより有効化できない場合は、自己判断でセキュリティ設定を変更せず講師へ相談してください。仮想環境を有効化しなくても、`uv run`でコマンドを実行できます。

### パッケージをインストール

```powershell
uv pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Flask-WTF tzdata
```

`tzdata`は、WindowsなどでIANAタイムゾーン情報を利用するための予備データです。

### バージョンを記録

```powershell
uv pip freeze > requirements.txt
```

`requirements.txt`へ記録すると、同じバージョンの環境を再現しやすくなります。`.venv`フォルダー自体は配布やGit管理に含めません。

---

## 5. 最小のFlaskアプリ

`app.py`を作ります。ファイル名を`flask.py`にするとFlaskパッケージと名前が衝突するため避けてください。

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>こんにちは、Flask！</h1>"
```

起動します。

```powershell
uv run flask --app app run --debug
```

ブラウザーで `http://127.0.0.1:5000/` を開きます。停止するときはターミナルで `Ctrl + C` を押します。

### コードの意味

```python
app = Flask(__name__)
```

Flaskアプリのインスタンスを作ります。`__name__`は、Flaskがテンプレートや静的ファイルなどの場所を判断するためにも使います。

```python
@app.route("/")
def index():
    return "..."
```

`/`というURLと`index()`関数を結び付けます。これをルーティングといいます。

### 開発サーバーの注意

- `--debug`は自動再読み込みとデバッガーを有効にする
- デバッガーはブラウザーからPythonコードを実行できる危険な機能を含む
- 開発サーバーとデバッグモードは公開環境で使わない
- `--host=0.0.0.0`は同じネットワークなどからアクセス可能にするため、授業で必要な場合だけ使う

---

## 6. ルーティングとURL

### 複数のページ

```python
@app.route("/")
def index():
    return "トップページ"


@app.route("/about")
def about():
    return "このアプリについて"
```

### URLから値を受け取る

```python
from markupsafe import escape


@app.route("/hello/<name>")
def hello(name):
    return f"{escape(name)}さん、こんにちは"


@app.route("/tasks/<int:task_id>")
def show_task(task_id):
    return f"タスクID: {task_id}"
```

`<int:task_id>`の`int`はURLコンバーターです。指定部分を整数として受け取ります。利用者の入力をHTML文字列へ直接埋め込む場合はエスケープが必要です。通常はJinjaテンプレートを利用します。

### url_for

URLを文字列で直接書かず、処理の名前から生成します。

```python
from flask import url_for

url_for("show_task", task_id=3)
```

結果は `/tasks/3` です。後からURLを変更しても、関数名が同じならリンクを修正せずに済みます。

---

## 7. Jinjaテンプレート

Pythonの文字列へ長いHTMLを書くのではなく、`templates`フォルダーへHTMLを置きます。CSS、JavaScript、画像などは`static`へ置きます。

```text
todo_application/
├─ app.py
├─ requirements.txt
├─ instance/
├─ static/
│  └─ style.css
└─ templates/
   ├─ base.html
   └─ hello.html
```

### Pythonから値を渡す

```python
from flask import render_template


@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)
```

`templates/hello.html`：

```html
{% extends "base.html" %}

{% block title %}あいさつ{% endblock %}

{% block content %}
  <h1>{{ name }}さん、こんにちは</h1>
{% endblock %}
```

- `{{ ... }}`：値を出力する
- `{% ... %}`：if、for、blockなどの処理を書く
- `{# ... #}`：Jinjaのコメント

HTMLテンプレートでは通常、自動エスケープが有効です。利用者の入力へ安易に`|safe`を付けてはいけません。

### テンプレート継承

`templates/base.html`：

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} - Todoアプリ</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <header>
      <a href="{{ url_for('index') }}">Todoアプリ</a>
    </header>
    <main>
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

共通のHTMLを`base.html`へまとめ、各ページでは必要なblockだけを置き換えます。

---

## 8. Todoアプリの設計

### 機能

- ユーザー登録
- ログイン・ログアウト
- 自分のタスク一覧
- タスクの追加
- タスク名と状態の編集
- タスクの削除
- 作成日時を日本時間で表示

### CRUD

| 操作 | 内容 | この教材のルート |
| --- | --- | --- |
| Create | タスクを作る | `POST /tasks/new` |
| Read | 一覧を読む | `GET /` |
| Update | タスクを直す | `POST /tasks/<id>/edit` |
| Delete | タスクを消す | `POST /tasks/<id>/delete` |

### データベース

```text
User（1人） ─────< Task（複数）

User
├─ id
├─ login_id
├─ password_hash
└─ created_at

Task
├─ id
├─ task_name
├─ status
├─ created_at
├─ updated_at
└─ user_id → User.id
```

パスワードそのものは保存せず、復元しにくいハッシュ値を保存します。

---

## 9. 完成版のフォルダー構成

```text
todo_application/
├─ .venv/                 # Gitや配布には含めない
├─ instance/              # SQLite DBが作られる
├─ static/
│  └─ style.css
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ login.html
│  ├─ register.html
│  └─ task_form.html
├─ app.py
└─ requirements.txt
```

まずは1つのPythonファイルで処理のつながりを学びます。規模が大きくなったら、アプリケーションファクトリー、Blueprint、モデルファイルなどへ分割します。

---

## 10. app.pyを作る

以下は教材用の完成コードです。長いため、章ごとに入力しながら動作を確認してください。

```python
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-before-publishing"),
    SQLALCHEMY_DATABASE_URI="sqlite:///todo.db",
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "ログインしてください。"

TASK_STATUSES = {
    "not_started": "未着手",
    "in_progress": "進行中",
    "completed": "完了",
    "pending": "保留",
}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="not_started",
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    user = db.relationship("User", back_populates="tasks")

    __table_args__ = (
        UniqueConstraint("user_id", "task_name", name="uq_user_task_name"),
    )


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


@app.template_filter("jst")
def format_jst(value):
    if value is None:
        return ""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M")


def get_owned_task_or_404(task_id):
    task = db.get_or_404(Task, task_id)
    if task.user_id != current_user.id:
        abort(403)
    return task


@app.route("/")
@login_required
def index():
    statement = (
        db.select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
    )
    tasks = db.session.execute(statement).scalars().all()
    return render_template(
        "index.html",
        tasks=tasks,
        task_statuses=TASK_STATUSES,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")

        if len(login_id) < 3 or len(login_id) > 100:
            flash("ログインIDは3〜100文字で入力してください。", "error")
        elif len(password) < 12:
            flash("パスワードは12文字以上にしてください。", "error")
        else:
            statement = db.select(User).where(User.login_id == login_id)
            existing_user = db.session.execute(statement).scalar_one_or_none()

            if existing_user:
                flash("そのログインIDは使用されています。", "error")
            else:
                user = User(login_id=login_id)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash("ユーザーを登録しました。ログインしてください。", "success")
                return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")
        statement = db.select(User).where(User.login_id == login_id)
        user = db.session.execute(statement).scalar_one_or_none()

        if user is None or not user.check_password(password):
            flash("ログインIDまたはパスワードが違います。", "error")
        else:
            login_user(user)
            flash("ログインしました。", "success")
            return redirect(url_for("index"))

    return render_template("login.html")


@app.post("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "success")
    return redirect(url_for("login"))


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def create_task():
    if request.method == "POST":
        task_name = request.form.get("task_name", "").strip()
        status = request.form.get("status", "not_started")

        if not task_name or len(task_name) > 100:
            flash("タスク名は1〜100文字で入力してください。", "error")
        elif status not in TASK_STATUSES:
            flash("正しい状態を選んでください。", "error")
        else:
            duplicate_statement = db.select(Task).where(
                Task.user_id == current_user.id,
                Task.task_name == task_name,
            )
            duplicate = db.session.execute(duplicate_statement).scalar_one_or_none()

            if duplicate:
                flash("同じ名前のタスクがすでにあります。", "error")
            else:
                task = Task(
                    task_name=task_name,
                    status=status,
                    user_id=current_user.id,
                )
                db.session.add(task)
                db.session.commit()
                flash("タスクを登録しました。", "success")
                return redirect(url_for("index"))

    return render_template(
        "task_form.html",
        page_title="タスクを作る",
        task=None,
        task_statuses=TASK_STATUSES,
    )


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = get_owned_task_or_404(task_id)

    if request.method == "POST":
        task_name = request.form.get("task_name", "").strip()
        status = request.form.get("status", "")

        if not task_name or len(task_name) > 100:
            flash("タスク名は1〜100文字で入力してください。", "error")
        elif status not in TASK_STATUSES:
            flash("正しい状態を選んでください。", "error")
        else:
            duplicate_statement = db.select(Task).where(
                Task.user_id == current_user.id,
                Task.task_name == task_name,
                Task.id != task.id,
            )
            duplicate = db.session.execute(duplicate_statement).scalar_one_or_none()

            if duplicate:
                flash("同じ名前のタスクがすでにあります。", "error")
            else:
                task.task_name = task_name
                task.status = status
                db.session.commit()
                flash("タスクを更新しました。", "success")
                return redirect(url_for("index"))

    return render_template(
        "task_form.html",
        page_title="タスクを編集する",
        task=task,
        task_statuses=TASK_STATUSES,
    )


@app.post("/tasks/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    task = get_owned_task_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("タスクを削除しました。", "success")
    return redirect(url_for("index"))
```

### 重要な修正点

- `password`ではなく`password_hash`へハッシュ値を保存
- 一覧はログイン中の利用者のタスクだけを取得
- 編集・削除時にも所有者を再確認
- `Model.query`ではなく`db.select()`と`db.session.execute()`を使用
- Enumへフォームの文字列を直接代入せず、許可した状態の辞書で検証
- 削除とログアウトはGETリンクではなくPOST
- すべてのPOSTフォームをCSRF保護
- 日時はUTCで保存し、表示時にJSTへ変換

---

## 11. テンプレートを作る

### base.html

`templates/base.html`：

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} - Todoアプリ</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <header class="site-header">
      <a class="site-title" href="{{ url_for('index') }}">Todoアプリ</a>

      {% if current_user.is_authenticated %}
        <span>{{ current_user.login_id }}さん</span>
        <form action="{{ url_for('logout') }}" method="post">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button type="submit">ログアウト</button>
        </form>
      {% endif %}
    </header>

    <main class="container">
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <div aria-live="polite">
            {% for category, message in messages %}
              <p class="flash flash-{{ category }}">{{ message }}</p>
            {% endfor %}
          </div>
        {% endif %}
      {% endwith %}

      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

### register.html

`templates/register.html`：

```html
{% extends "base.html" %}

{% block title %}ユーザー登録{% endblock %}

{% block content %}
  <h1>ユーザー登録</h1>

  <form method="post" class="card">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

    <label for="login_id">ログインID</label>
    <input id="login_id" name="login_id" minlength="3" maxlength="100" required>

    <label for="password">パスワード（12文字以上）</label>
    <input id="password" name="password" type="password" minlength="12" required>

    <button type="submit">登録する</button>
  </form>

  <p><a href="{{ url_for('login') }}">登録済みの人はログイン</a></p>
{% endblock %}
```

### login.html

`templates/login.html`：

```html
{% extends "base.html" %}

{% block title %}ログイン{% endblock %}

{% block content %}
  <h1>ログイン</h1>

  <form method="post" class="card">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

    <label for="login_id">ログインID</label>
    <input id="login_id" name="login_id" autocomplete="username" required>

    <label for="password">パスワード</label>
    <input
      id="password"
      name="password"
      type="password"
      autocomplete="current-password"
      required
    >

    <button type="submit">ログインする</button>
  </form>

  <p><a href="{{ url_for('register') }}">ユーザーを登録する</a></p>
{% endblock %}
```

### index.html

`templates/index.html`：

```html
{% extends "base.html" %}

{% block title %}タスク一覧{% endblock %}

{% block content %}
  <div class="page-heading">
    <h1>タスク一覧</h1>
    <a class="button" href="{{ url_for('create_task') }}">新しいタスク</a>
  </div>

  {% if tasks %}
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th scope="col">タスク名</th>
            <th scope="col">状態</th>
            <th scope="col">作成日時</th>
            <th scope="col">操作</th>
          </tr>
        </thead>
        <tbody>
          {% for task in tasks %}
            <tr>
              <td>{{ task.task_name }}</td>
              <td>{{ task_statuses[task.status] }}</td>
              <td><time datetime="{{ task.created_at.isoformat() }}">{{ task.created_at|jst }}</time></td>
              <td class="actions">
                <a href="{{ url_for('edit_task', task_id=task.id) }}">編集</a>

                <form
                  action="{{ url_for('delete_task', task_id=task.id) }}"
                  method="post"
                  onsubmit="return confirm('このタスクを削除しますか？');"
                >
                  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                  <button type="submit" class="danger">削除</button>
                </form>
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  {% else %}
    <p>タスクはまだありません。</p>
  {% endif %}
{% endblock %}
```

### task_form.html

`templates/task_form.html`：

```html
{% extends "base.html" %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
  <h1>{{ page_title }}</h1>

  <form method="post" class="card">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

    <label for="task_name">タスク名</label>
    <input
      id="task_name"
      name="task_name"
      maxlength="100"
      value="{{ task.task_name if task else '' }}"
      required
    >

    <label for="status">状態</label>
    <select id="status" name="status">
      {% for value, label in task_statuses.items() %}
        <option
          value="{{ value }}"
          {% if task and task.status == value %}selected{% endif %}
        >
          {{ label }}
        </option>
      {% endfor %}
    </select>

    <button type="submit">保存する</button>
  </form>

  <p><a href="{{ url_for('index') }}">一覧へ戻る</a></p>
{% endblock %}
```

---

## 12. CSSを作る

`static/style.css`：

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: #1f2937;
  background: #f1f5f9;
  font-family: system-ui, sans-serif;
  line-height: 1.6;
}

a {
  color: #1d4ed8;
}

button,
input,
select {
  font: inherit;
}

button,
.button {
  display: inline-block;
  padding: 0.6rem 0.9rem;
  border: 0;
  border-radius: 0.4rem;
  color: white;
  background: #1d4ed8;
  cursor: pointer;
  text-decoration: none;
}

button.danger {
  background: #b91c1c;
}

a:focus-visible,
button:focus-visible,
input:focus-visible,
select:focus-visible {
  outline: 3px solid #f59e0b;
  outline-offset: 3px;
}

.site-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  color: white;
  background: #0f172a;
}

.site-header form {
  margin-left: auto;
}

.site-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
}

.container {
  width: min(100% - 2rem, 64rem);
  margin-inline: auto;
  padding-block: 2rem;
}

.page-heading,
.actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
}

.page-heading {
  justify-content: space-between;
}

.card {
  display: grid;
  gap: 0.75rem;
  max-width: 32rem;
  padding: 1.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.75rem;
  background: white;
}

input,
select {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #64748b;
  border-radius: 0.4rem;
}

.flash {
  padding: 0.75rem;
  border-left: 0.3rem solid;
  background: white;
}

.flash-success {
  border-color: #15803d;
}

.flash-error {
  border-color: #b91c1c;
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th,
td {
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  text-align: left;
}
```

---

## 13. データベースを作る

### マイグレーションを準備

最初の1回だけ実行します。

```powershell
uv run flask --app app db init
```

モデルの構造をマイグレーションファイルに記録します。

```powershell
uv run flask --app app db migrate -m "create user and task tables"
```

データベースへ反映します。

```powershell
uv run flask --app app db upgrade
```

`instance/todo.db`が作成されます。

### モデルを変更したとき

```powershell
uv run flask --app app db migrate -m "describe the change"
uv run flask --app app db upgrade
```

自動生成されたマイグレーションは、実行前に内容を確認します。モデル変更をすべて完全に判断できるわけではありません。

---

## 14. アプリを起動する

```powershell
uv run flask --app app run --debug
```

`http://127.0.0.1:5000/register`を開き、次の順番で確認します。

1. ユーザーを登録する
2. 登録したユーザーでログインする
3. タスクを作る
4. 一覧へ表示されることを確認する
5. タスク名と状態を編集する
6. タスクを削除する
7. ログアウトする

---

## 15. データベース操作を読む

### Create

```python
task = Task(task_name="宿題", user_id=current_user.id)
db.session.add(task)
db.session.commit()
```

### Read

```python
statement = db.select(Task).where(Task.user_id == current_user.id)
tasks = db.session.execute(statement).scalars().all()
```

### Update

```python
task.task_name = "数学の宿題"
db.session.commit()
```

### Delete

```python
db.session.delete(task)
db.session.commit()
```

変更は`commit()`で確定します。途中で例外が起きた場合は、実際のアプリではログを残し、必要に応じて`db.session.rollback()`でトランザクションを戻す設計も必要です。

---

## 16. UTCとJST

複数地域から利用するWebアプリでは、データベースにUTCで保存し、画面表示時に利用者のタイムゾーンへ変換すると扱いやすくなります。

```python
created_at = db.Column(
    db.DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    nullable=False,
)
```

Jinjaフィルターで日本時間へ変換します。

```python
@app.template_filter("jst")
def format_jst(value):
    if value is None:
        return ""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M")
```

テンプレート：

```html
{{ task.created_at|jst }}
```

### replaceとastimezoneの違い

- `replace(tzinfo=...)`：時計の数字を変えず、どのタイムゾーンの値かという情報を付ける
- `astimezone(...)`：同じ時刻を別のタイムゾーンの時計表示へ変換する

元データが本当にUTCだと確認できる場合だけ`replace(tzinfo=timezone.utc)`を使います。すでに日本時間の値へUTCラベルを付けると9時間ずれます。

`timezone(timedelta(hours=9))`でも現在のJSTは表せますが、地域名を明示できる`ZoneInfo("Asia/Tokyo")`をこの教材では使います。

---

## 17. セキュリティで重要なこと

### パスワード

- 平文で保存しない
- `generate_password_hash()`で保存用の値を作る
- `check_password_hash()`で照合する
- ログや画面へパスワードを出さない
- 公開アプリでは十分な長さ、レート制限、MFAなども検討する

### SECRET_KEY

セッションやCSRFトークンの署名などに使われます。公開環境では推測できないランダムな値を環境変数から設定し、Gitへ登録しません。

PowerShellで開発用の一時値を設定する例：

```powershell
$env:SECRET_KEY = "授業で指定されたランダムな値"
```

### CSRF

ログイン中の利用者に、別サイトから意図しないPOST操作をさせる攻撃をCSRFといいます。Flask-WTFの`CSRFProtect`と、フォーム内のトークンで対策します。

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

### 認証と認可

- **認証**：だれなのかを確かめる
- **認可**：その人がその操作をしてよいか確かめる

`@login_required`はログインを要求しますが、それだけでは他人のタスク操作を防げません。取得後に`task.user_id == current_user.id`も確認します。

### 入力検証

HTMLの`required`や`maxlength`は便利ですが、リクエストを直接送れば回避できます。サーバー側でも空文字、長さ、許可する選択肢、権限を検証します。

---

## 18. よくあるエラー

### flaskコマンドが見つからない

仮想環境が違う可能性があります。

```powershell
uv run flask --app app run --debug
```

### ModuleNotFoundError

現在の環境へパッケージが入っているか確認します。

```powershell
uv pip list
```

### TemplateNotFound

- フォルダー名が`templates`か
- ファイル名の綴りと大文字・小文字が一致しているか
- `app.py`と`templates`の位置関係が正しいか

### CSSが反映されない

- CSSが`static/style.css`にあるか
- `url_for('static', filename='style.css')`を使っているか
- 保存後に再読み込みしたか

### 404 Not Found

- ルートのURLとブラウザーのURLが一致しているか
- `<int:task_id>`へ整数を渡しているか
- 対象データが存在するか

### 405 Method Not Allowed

ルートが受け付けるメソッドとフォームの`method`が一致していません。

### 400 Bad Request / CSRFエラー

POSTフォームへCSRFトークンがあるか、セッションが有効か確認します。CSRF保護を無効化して解決しないでください。

### 500 Internal Server Error

ターミナルのトレースバックを下から読みます。変数名、属性名、インデント、データ型、データベース構造を確認します。公開環境では利用者へ詳細なトレースバックを見せません。

### 日時が表示されない・ずれる

- テンプレートが`created_at`を参照しているか
- 存在しない`time_stamp`を参照していないか
- 保存値がUTCか
- naive datetimeへUTC情報を付ける前に、元の意味を確認したか

---

## 19. 動作テスト

### 基本機能

- [ ] ユーザーを登録できる
- [ ] 同じログインIDを登録できない
- [ ] 正しい情報でログインできる
- [ ] 誤ったパスワードでログインできない
- [ ] 未ログインで一覧を開くとログイン画面へ移動する
- [ ] タスクを登録できる
- [ ] 同じ利用者は同名タスクを重複登録できない
- [ ] 別の利用者は同じタスク名を登録できる
- [ ] タスクを編集できる
- [ ] タスクを削除できる
- [ ] ログアウトできる

### セキュリティ

- [ ] パスワードがDBへ平文保存されていない
- [ ] 他人のタスクが一覧へ表示されない
- [ ] 他人のタスクIDをURLへ入れても編集・削除できない
- [ ] CSRFトークンなしのPOSTが拒否される
- [ ] タスク名へHTMLを書いてもコードとして実行されない
- [ ] GETアクセスだけで登録・更新・削除されない

### 表示

- [ ] 作成日時が日本時間として表示される
- [ ] タスクが0件でも画面が崩れない
- [ ] 長いタスク名を適切に拒否する
- [ ] キーボードでフォームとボタンを操作できる
- [ ] 狭い画面でも操作できる

---

## 20. 発展課題

- タスクの期限を追加する
- 状態で絞り込む
- タスク名で検索する
- 完了・未完了をワンクリックで切り替える
- ページ分割を追加する
- Flask-WTFの`FlaskForm`クラスでフォームを定義する
- Blueprintで認証とタスク機能を分割する
- 自動テストを作る
- 本番用WSGIサーバーとホスティングサービスで公開する

> Flaskの開発サーバーは公開用ではありません。本番環境では、ホスティングサービスの手順に従い、本番用WSGIサーバー、HTTPS、秘密情報の管理、ログ、バックアップなどを設定します。

---

## 21. 確認問題

1. Flaskは何をするためのフレームワークですか。
2. 仮想環境をプロジェクトごとに作る理由は何ですか。
3. ルーティングとは何ですか。
4. GETで削除処理を作らない理由は何ですか。
5. Jinjaの`{{ ... }}`と`{% ... %}`は何が違いますか。
6. CSSファイルは`templates`と`static`のどちらへ置きますか。
7. CRUDの4操作を挙げてください。
8. パスワードを平文で保存してはいけない理由は何ですか。
9. 認証と認可の違いは何ですか。
10. 日時をUTCで保存する利点は何ですか。

<details>
<summary>解答例</summary>

1. PythonでWebアプリのサーバー側処理を作るため。
2. パッケージやバージョンの衝突を減らし、環境を再現しやすくするため。
3. URLと実行するPython関数を結び付けること。
4. GETは情報取得に使うもので、リンクの先読みや誤操作だけで削除される危険があるため。
5. `{{ ... }}`は値の出力、`{% ... %}`はif、for、blockなどの処理。
6. `static`。
7. Create、Read、Update、Delete。
8. DBが漏えいしたとき、利用者のパスワードそのものを知られないようにするため。
9. 認証は本人確認、認可はその操作を許可するかの確認。
10. 地域に依存しない基準で保存し、表示時に各地域の時刻へ変換しやすくするため。

</details>

---

## まとめ

- FlaskはPython製のWebフレームワーク
- ルーティングでURL、HTTPメソッド、Python関数を結び付ける
- JinjaテンプレートでHTMLとPythonのデータを組み合わせる
- HTMLは`templates`、CSS・JavaScript・画像は`static`へ置く
- SQLAlchemyでCRUDを行い、変更は`commit()`で確定する
- POST後はリダイレクトし、再送信を防ぐ
- パスワードはハッシュ化し、POSTフォームはCSRFから保護する
- ログインだけでなく、対象データを操作する権限も確認する
- 日時はUTC保存、表示時に`ZoneInfo`でJSTへ変換する
- デバッグサーバーを本番環境で使わない

## 参考資料

### 元教材

- [Flask開発の環境構築](https://app.notion.com/p/323b4d0374118094a954c4b0bbe0098e)
- [Flaskのチュートリアル](https://app.notion.com/p/323b4d0374118002a6fee2174d5fa45a)
- [HTTPリクエスト](https://app.notion.com/p/323b4d03741180688da4cb76e1e3ff52)
- [FlaskでTodoアプリを作成する](https://app.notion.com/p/323b4d03741180eba4b9ef402dbde9bf)
- [日付の表示をする方法](https://app.notion.com/p/339b4d03741180c6853ae3e1d493f615)

### 公式資料

- [Flask Documentation「Quickstart」](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Flask Documentation「Tutorial」](https://flask.palletsprojects.com/en/stable/tutorial/)
- [Flask Documentation「Deploying to Production」](https://flask.palletsprojects.com/en/stable/deploying/)
- [Flask-SQLAlchemy「Modifying and Querying Data」](https://flask-sqlalchemy.palletsprojects.com/en/stable/queries/)
- [Python Documentation「zoneinfo」](https://docs.python.org/3/library/zoneinfo.html)

※Flask、Python、拡張機能の仕様や対応バージョンは変わります。実際に利用するときは、授業の指定と各公式ドキュメントの最新版を確認してください。
