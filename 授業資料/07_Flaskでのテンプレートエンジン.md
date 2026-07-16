# Flaskでのテンプレートエンジン

> Webアプリ作成講座｜配布用教材 07

この教材では、Flaskで利用するテンプレートエンジン「Jinja」の基本を学びます。PythonからHTMLへデータを渡し、条件分岐や繰り返し、テンプレート継承を使って、管理しやすいWebページを作ります。

---

## 1. 今日のゴール

この教材を終えると、次のことができるようになります。

- テンプレートエンジンの役割を説明できる
- FlaskからHTMLへ文字列・辞書・リストを渡せる
- Jinjaの変数、条件分岐、繰り返しを使える
- 共通部分を`base.html`へまとめられる
- `url_for()`を使ってURLを安全に組み立てられる
- ブラウザーから送られたクエリ文字列を受け取れる

---

## 2. テンプレートエンジンとは

テンプレートエンジンは、**HTMLのひな型とPythonのデータを組み合わせ、完成したHTMLを作る仕組み**です。

たとえば、ログインした人の名前によって表示を変えるページを考えます。

```text
HTMLのひな型 ＋ Pythonのデータ → 完成したHTML → ブラウザーへ送信
              「さくら」          「こんにちは、さくらさん」
```

HTMLだけで作ったページは、基本的に保存されている内容をそのまま表示します。テンプレートを使うと、商品一覧、Todo一覧、ログイン中のユーザー名など、状況に応じた内容を表示できます。

Flaskは特定のMVC／MVT構成を強制しません。Jinjaは画面表示を担当する仕組みとして使えますが、「必ずMVTモデルのTに当たる」と決まっているわけではありません。

### Jinjaとは

Flaskは標準のテンプレートエンジンとして**Jinja**を利用します。以前は「Jinja2」という呼び方がよく使われていましたが、現在の正式なプロジェクト名は「Jinja」です。

JinjaのコードはHTMLの中に書きます。ただし、Pythonそのものではなく、Jinja専用の文法です。

---

## 3. テンプレートを使う準備

次のフォルダーとファイルを作ります。

```text
jinja_lesson/
├─ app.py
├─ templates/
│  ├─ base.html
│  ├─ home.html
│  └─ next.html
└─ static/
   └─ style.css
```

- HTMLファイルは`templates`フォルダーへ置く
- CSS、画像、JavaScriptなどは`static`フォルダーへ置く
- フォルダー名は原則としてこの名前を使う

### app.py

```python
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", title="ホーム")


@app.route("/next")
def next_page():
    return render_template("next.html", title="次のページ")
```

`render_template()`は、`templates`フォルダーから指定したHTMLを探し、Jinjaで処理してからブラウザーへ返します。

```python
return render_template("home.html", title="ホーム")
```

この例では、`title`という名前で文字列`"ホーム"`をテンプレートへ渡しています。

---

## 4. Jinjaの基本記号

Jinjaでは、おもに次の3種類の記号を使います。

| 書き方 | 役割 | 例 |
| --- | --- | --- |
| `{{ ... }}` | 値や計算結果を表示する | `{{ title }}` |
| `{% ... %}` | `if`、`for`、継承などの処理を書く | `{% if user %}` |
| `{# ... #}` | テンプレート内にコメントを書く | `{# 見出し #}` |

### 値を表示する

```html
<h1>{{ title }}</h1>
```

`app.py`から渡した`title`の値が`{{ title }}`の位置へ入ります。一般的には、記号の内側へ空白を入れると読みやすくなります。

### HTMLコメントとの違い

```html
<!-- HTMLコメント：ブラウザーへ送られる -->
{# Jinjaコメント：完成したHTMLには含まれない #}
```

秘密情報は、どちらのコメントにも書かないようにしましょう。

---

## 5. Pythonからさまざまな値を渡す

### 複数の値

```python
@app.route("/")
def home():
    return render_template(
        "home.html",
        title="ホーム",
        message="Jinjaを練習しましょう。",
        lesson_number=7,
    )
```

```html
<h1>{{ title }}</h1>
<p>{{ message }}</p>
<p>教材番号：{{ lesson_number }}</p>
```

### 辞書

関連する複数の値は、辞書にまとめられます。

```python
@app.route("/")
def home():
    page = {
        "title": "ホーム",
        "message": "これはホームページです。",
    }
    return render_template("home.html", page=page)
```

```html
<h1>{{ page.title }}</h1>
<p>{{ page.message }}</p>
```

Jinjaでは`page.title`のようにドットで辞書の値を参照できます。Pythonと同じ形に近づけたい場合は、`page["title"]`とも書けます。

> 辞書は複数のデータに不向きなのではありません。辞書は「1件のデータが持つ項目」を表すのが得意で、リストは「同じ種類のデータが複数ある状態」を表すのが得意です。実際のWebアプリでは、辞書を並べたリストもよく使います。

### リスト

```python
@app.route("/")
def home():
    members = ["あおい", "はる", "ゆうき"]
    return render_template("home.html", title="メンバー一覧", members=members)
```

リストのすべての値を表示するときは、Jinjaの`for`を使います。

```html
<h1>{{ title }}</h1>

<ul>
  {% for member in members %}
    <li>{{ member }}</li>
  {% endfor %}
</ul>
```

Jinjaの処理はインデントではなく、`{% endfor %}`などの終了タグで範囲を表します。ただし、読みやすくするためにインデントもそろえましょう。

### 辞書を並べたリスト

```python
@app.route("/")
def home():
    tasks = [
        {"title": "HTMLを復習する", "done": True},
        {"title": "Jinjaを練習する", "done": False},
        {"title": "課題を提出する", "done": False},
    ]
    return render_template("home.html", title="Todo一覧", tasks=tasks)
```

```html
<ul>
  {% for task in tasks %}
    <li>{{ task.title }}：{{ task.done }}</li>
  {% endfor %}
</ul>
```

---

## 6. 条件によって表示を変える

Jinjaの`if`を使うと、データによって表示を変えられます。

```html
{% if is_logged_in %}
  <p>ログインしています。</p>
{% else %}
  <p>ログインしてください。</p>
{% endif %}
```

複数の条件を調べる場合は`elif`を使います。

```html
{% if score >= 80 %}
  <p>よくできました！</p>
{% elif score >= 60 %}
  <p>合格です。</p>
{% else %}
  <p>もう一度復習しましょう。</p>
{% endif %}
```

### `for`と`else`

リストが空の場合の表示も用意できます。

```html
<ul>
  {% for task in tasks %}
    <li>{{ task.title }}</li>
  {% else %}
    <li>タスクはまだありません。</li>
  {% endfor %}
</ul>
```

これは、一覧画面でよく使う書き方です。

### 繰り返し回数を表示する

`loop.index`は1から始まる繰り返し番号です。

```html
{% for member in members %}
  <p>{{ loop.index }}人目：{{ member }}</p>
{% endfor %}
```

---

## 7. フィルターで表示を整える

フィルターは、値の表示方法を変える機能です。値の後ろに`|`とフィルター名を書きます。

```html
{{ value | フィルター名 }}
```

| フィルター | 役割 | 使用例 |
| --- | --- | --- |
| `length` | 要素数や文字数を数える | `{{ members | length }}` |
| `upper` | 英字を大文字にする | `{{ name | upper }}` |
| `lower` | 英字を小文字にする | `{{ name | lower }}` |
| `default` | 値が未定義のときの表示を決める | `{{ nickname | default("未設定") }}` |
| `join` | リストを指定した文字でつなぐ | `{{ tags | join(", ") }}` |

例：

```html
<p>メンバーは{{ members | length }}人です。</p>
```

複雑なデータ加工はJinjaへ詰め込まず、Python側で処理してからテンプレートへ渡すと読みやすくなります。

---

## 8. テンプレート継承

Webサイトには、どのページにも共通する部分があります。

- HTML全体の基本構造
- ヘッダーやナビゲーション
- CSSの読み込み
- フッター

すべてのHTMLへ同じコードを書くと、リンクを1つ変更するだけで全ファイルを直す必要があります。そこで、共通部分を`base.html`へまとめ、ページごとに違う部分だけを子テンプレートへ書きます。これを**テンプレート継承**といいます。

### 継承元：base.html

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Jinja練習{% endblock %}</title>
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='style.css') }}"
    >
  </head>
  <body>
    <header>
      <nav>
        <a href="{{ url_for('home') }}">ホーム</a>
        <a href="{{ url_for('next_page') }}">次のページ</a>
      </nav>
    </header>

    <main>
      {% block content %}{% endblock %}
    </main>

    <footer>
      <small>Webアプリ作成講座</small>
    </footer>
  </body>
</html>
```

`block`は、子テンプレートが内容を入れ替えられる場所です。この例では`title`と`content`の2つを用意しています。

### 継承先：home.html

```html
{% extends "base.html" %}

{% block title %}{{ title }}｜Jinja練習{% endblock %}

{% block content %}
  <h1>{{ title }}</h1>
  <p>これはホームページです。</p>
{% endblock %}
```

### 継承先：next.html

```html
{% extends "base.html" %}

{% block title %}{{ title }}｜Jinja練習{% endblock %}

{% block content %}
  <h1>{{ title }}</h1>
  <p>これは次のページです。</p>
{% endblock %}
```

`{% extends "base.html" %}`は、原則として子テンプレートの先頭に書きます。子テンプレートの各`block`名は、`base.html`の対応する`block`名と同じにします。

---

## 9. url_forでURLを作る

`url_for()`は、Flaskの**エンドポイント名からURLを生成する関数**です。通常、エンドポイント名にはビュー関数の名前を使います。

```python
@app.route("/")
def home():
    return render_template("home.html")
```

```html
<a href="{{ url_for('home') }}">ホームへ戻る</a>
```

この場合、`url_for('home')`は`/`を生成します。

### URLを直接書かない理由

```html
<!-- URLを直接書く方法 -->
<a href="/">ホーム</a>

<!-- url_forを使う方法 -->
<a href="{{ url_for('home') }}">ホーム</a>
```

ルートのURLを後から変更しても、関数名が同じならテンプレートを直さずに済みます。Blueprintを使う場合は、`url_for('main.home')`のようにエンドポイント名が変わることがあります。

### CSSのURL

`static`フォルダーのファイルにも`url_for()`を使います。

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### URLへ値を渡す

ルートにURL変数がある場合は、その値を指定します。

```python
@app.route("/users/<int:user_id>")
def user_detail(user_id):
    return render_template("user_detail.html", user_id=user_id)
```

```html
<a href="{{ url_for('user_detail', user_id=3) }}">ユーザー3を見る</a>
```

生成されるURL：

```text
/users/3
```

ルートにない値を渡すと、クエリ文字列になります。

```html
<a href="{{ url_for('next_page', title='Jinjaの練習') }}">次へ</a>
```

生成例：

```text
/next?title=Jinja%E3%81%AE%E7%B7%B4%E7%BF%92
```

日本語などはURLで安全に使える形へ変換されます。ブラウザーやFlaskが読み取ると、元の文字列として扱えます。

---

## 10. クエリ文字列を受け取る

URLの`?`より後ろを**クエリ文字列**といいます。

```text
/next?title=Jinja
       └─ キー：title、値：Jinja
```

Flaskでは`request.args.get()`で受け取ります。

```python
@app.route("/next")
def next_page():
    title = request.args.get("title", "次のページ")
    return render_template("next.html", title=title)
```

第2引数の`"次のページ"`は、`title`が送られなかった場合の初期値です。

```html
<h1>{{ title }}</h1>
```

### URL変数との違い

| 種類 | URL例 | Flaskでの受け取り方 | 向いている用途 |
| --- | --- | --- | --- |
| URL変数 | `/users/3` | ビュー関数の引数 | 表示対象を特定するIDなど |
| クエリ文字列 | `/users?sort=name` | `request.args.get()` | 検索、並び替え、絞り込みなど |

クエリ文字列はURLに表示され、履歴やサーバーの記録へ残る場合があります。パスワードなどの秘密情報を入れてはいけません。また、受け取った値を信用せず、Python側で長さや形式を確認します。

---

## 11. 完成版を作る

ここまでの内容を組み合わせ、講座一覧を表示する小さなアプリを作ります。

### app.py

```python
from flask import Flask, render_template, request


app = Flask(__name__)


LESSONS = [
    {"title": "HTMLの基礎", "completed": True},
    {"title": "CSSの基礎", "completed": True},
    {"title": "Jinjaの基礎", "completed": False},
]


@app.route("/")
def home():
    page = {
        "title": "講座一覧",
        "message": "学習中の教材を確認しましょう。",
    }
    return render_template("home.html", page=page, lessons=LESSONS)


@app.route("/next")
def next_page():
    title = request.args.get("title", "次のページ")
    return render_template("next.html", title=title)
```

### templates/base.html

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Webアプリ作成講座{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <header class="site-header">
      <nav class="container">
        <a href="{{ url_for('home') }}">講座一覧</a>
        <a href="{{ url_for('next_page') }}">次のページ</a>
      </nav>
    </header>

    <main class="container">
      {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
      <small>Webアプリ作成講座</small>
    </footer>
  </body>
</html>
```

### templates/home.html

```html
{% extends "base.html" %}

{% block title %}{{ page.title }}｜Webアプリ作成講座{% endblock %}

{% block content %}
  <h1>{{ page.title }}</h1>
  <p>{{ page.message }}</p>

  <p>教材数：{{ lessons | length }}</p>

  <ul class="lesson-list">
    {% for lesson in lessons %}
      <li>
        <span>{{ loop.index }}. {{ lesson.title }}</span>
        {% if lesson.completed %}
          <strong class="completed">学習済み</strong>
        {% else %}
          <span>学習中</span>
        {% endif %}
      </li>
    {% else %}
      <li>教材はまだありません。</li>
    {% endfor %}
  </ul>

  <a href="{{ url_for('next_page', title='Jinjaの確認問題') }}">
    確認問題へ進む
  </a>
{% endblock %}
```

### templates/next.html

```html
{% extends "base.html" %}

{% block title %}{{ title }}｜Webアプリ作成講座{% endblock %}

{% block content %}
  <h1>{{ title }}</h1>
  <p>テンプレートの使い方を確認できましたか？</p>
  <a href="{{ url_for('home') }}">講座一覧へ戻る</a>
{% endblock %}
```

### static/style.css

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: #1f2937;
  font-family: system-ui, sans-serif;
  background: #f8fafc;
}

.container {
  width: min(90%, 800px);
  margin-inline: auto;
}

.site-header {
  padding: 1rem 0;
  background: #1d4ed8;
}

.site-header nav {
  display: flex;
  gap: 1rem;
}

.site-header a {
  color: #ffffff;
}

main {
  min-height: 75vh;
  padding-block: 2rem;
}

.lesson-list {
  padding: 0;
  list-style: none;
}

.lesson-list li {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  margin-bottom: 0.75rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
}

.completed {
  color: #15803d;
}

.site-footer {
  padding: 1rem;
  text-align: center;
  background: #e2e8f0;
}
```

### 起動する

仮想環境を有効にした状態で、次のコマンドを実行します。

```powershell
flask --app app run --debug
```

ブラウザーで`http://127.0.0.1:5000/`を開きます。`--debug`は開発中だけ使用し、インターネットへ公開する環境では使用しません。

---

## 12. 自動エスケープと安全性

Flaskで`.html`テンプレートを`render_template()`によって表示すると、Jinjaの**自動エスケープ**が有効になります。

たとえば、入力された文字列が次の場合を考えます。

```html
<script>alert("危険")</script>
```

`{{ message }}`で表示すると、JinjaはHTMLとして実行されない文字へ変換します。これはクロスサイトスクリプティング（XSS）対策として重要です。

```html
<p>{{ message }}</p>
```

`|safe`を付けると、自動エスケープを無効にしてHTMLとして扱います。

```html
{{ message | safe }}
```

利用者が入力した値や、信頼できるか分からない値には`|safe`を付けてはいけません。HTMLを表示する必要がある場合も、サーバー側で安全性を確認した値だけを使用します。

---

## 13. 役割を分ける

Webアプリを読みやすくするため、処理を次のように分けます。

| 場所 | おもな役割 |
| --- | --- |
| Python | データ取得、入力検証、計算、データベース操作 |
| Jinja | 受け取ったデータをHTMLへ配置、簡単な分岐や繰り返し |
| HTML | ページの意味と構造 |
| CSS | 色、余白、配置などの見た目 |

Jinjaで複雑な計算やデータベース操作をしようとせず、必要なデータをPython側で準備してから渡すのが基本です。

---

## 14. よくあるエラー

### TemplateNotFound

```text
jinja2.exceptions.TemplateNotFound: home.html
```

確認すること：

- フォルダー名が`templates`になっているか
- `home.html`が`templates`の中にあるか
- ファイル名の大文字・小文字や拡張子が正しいか
- `render_template("home.html")`の名前と一致しているか

### BuildError

```text
werkzeug.routing.exceptions.BuildError
```

`url_for()`に指定したエンドポイント名が見つからないときなどに発生します。

```html
{{ url_for('home') }}
```

ビュー関数が`def home():`になっているか確認します。URLの`/`ではなく、通常は**関数名**を指定します。

### UndefinedError

テンプレートで使った変数が渡されていない、または名前が違う可能性があります。

```python
render_template("home.html", title="ホーム")
```

```html
<!-- titleと同じ名前にする -->
<h1>{{ title }}</h1>
```

### CSSが反映されない

CSSを`templates`ではなく`static`フォルダーへ置き、次の形で読み込みます。

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### blockの内容が表示されない

- 親と子で`block`名が一致しているか
- `{% endblock %}`を書き忘れていないか
- 子テンプレートの先頭に`{% extends "base.html" %}`があるか

---

## 15. 練習問題

### 問題1：値を表示する

Pythonから`student_name="あおい"`を渡し、HTMLに「あおいさん、こんにちは」と表示してください。

<details>
<summary>解答例</summary>

```python
return render_template("home.html", student_name="あおい")
```

```html
<p>{{ student_name }}さん、こんにちは</p>
```

</details>

### 問題2：条件分岐

`score`が60以上なら「合格」、それ以外なら「再挑戦」と表示してください。

<details>
<summary>解答例</summary>

```html
{% if score >= 60 %}
  <p>合格</p>
{% else %}
  <p>再挑戦</p>
{% endif %}
```

</details>

### 問題3：繰り返し

`languages = ["HTML", "CSS", "Python"]`のすべての値をリスト表示してください。

<details>
<summary>解答例</summary>

```html
<ul>
  {% for language in languages %}
    <li>{{ language }}</li>
  {% endfor %}
</ul>
```

</details>

### 問題4：URL生成

ビュー関数`profile`へ、URL変数`user_id=5`を渡すリンクを書いてください。

<details>
<summary>解答例</summary>

```html
<a href="{{ url_for('profile', user_id=5) }}">プロフィール</a>
```

</details>

### 発展課題

- 講座一覧へ新しい教材を追加する
- 学習済みと学習中で別のCSSクラスを付ける
- `base.html`へ現在の年を表示する
- 検索語をクエリ文字列で送り、Python側で一覧を絞り込む
- 共通する小さな部品を`{% include "部品名.html" %}`で別ファイルに分ける

---

## 16. まとめ

- テンプレートエンジンはHTMLのひな型とデータを組み合わせる
- FlaskはJinjaを標準のテンプレートエンジンとして利用する
- `{{ ... }}`は値の表示、`{% ... %}`は処理に使う
- `if`で条件分岐、`for`で繰り返しができる
- 共通部分は`base.html`へまとめ、テンプレート継承を使う
- URLは`url_for()`でエンドポイント名から生成する
- クエリ文字列は`request.args.get()`で受け取る
- 複雑な処理や入力検証はPython側で行う
- 自動エスケープを保ち、信頼できない値に`|safe`を使わない

---

## 参考資料

### 元教材

- [Flaskでのテンプレートエンジン（Jinja）](https://app.notion.com/p/323b4d03741180d78c48c66fba3658d0)

### 公式資料

- [Flask公式ドキュメント：Templates](https://flask.palletsprojects.com/en/stable/templating/)
- [Flask公式チュートリアル：Templates](https://flask.palletsprojects.com/en/stable/tutorial/templates/)
- [Jinja公式ドキュメント：Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/)
