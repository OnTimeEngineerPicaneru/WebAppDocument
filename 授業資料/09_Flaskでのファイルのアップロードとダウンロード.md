# Flaskでのファイルのアップロードとダウンロード

> Webアプリ作成講座｜配布用教材 09

この教材では、ブラウザーから画像をアップロードし、保存した画像の表示とダウンロードができるFlaskアプリを作ります。ファイルは文字列よりも慎重に扱う必要があるため、安全なファイル名、容量制限、内容の検査なども学びます。

---

## 1. 今日のゴール

- HTTPでファイルを送受信できることを説明できる
- HTMLのファイル選択フォームを作れる
- `request.files`からアップロードファイルを取得できる
- ファイル名、種類、容量を検査して保存できる
- `send_from_directory()`でファイルを表示・ダウンロードできる
- ファイルアップロードのおもな危険と対策を説明できる

---

## 2. HTTPでファイルを送る仕組み

HTTPで送受信できるのは文章だけではありません。画像、PDF、音声、動画なども、最終的にはバイト列というデータとして送受信できます。

ブラウザーからファイルを送るときは、通常は次の流れになります。

```text
1. 利用者がフォームでファイルを選ぶ
2. ブラウザーがPOSTリクエストでファイルを送る
3. Flaskがファイルを検査する
4. 問題がなければサーバーへ保存する
5. 結果ページへリダイレクトする
```

### multipart/form-data

ファイルを送るフォームには、`enctype="multipart/form-data"`が必要です。

```html
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <button type="submit">アップロード</button>
</form>
```

これにより、通常の文字列とファイルデータを複数の部分に分けて送信できます。`enctype`を書き忘れると、Flaskはファイル本体を受け取れません。

---

## 3. 完成するアプリ

この教材では、次の機能を作ります。

- PNG、JPEG、GIF画像のアップロード
- 保存済み画像の一覧表示
- ブラウザー内での画像表示
- 添付ファイルとしてのダウンロード
- 5 MiBを超えるリクエストの拒否
- CSRF対策

> この教材では画像だけを扱います。PDFなども扱う場合は、許可する形式と検査方法を別途決める必要があります。

---

## 4. 開発環境を準備する

前の教材で作った仮想環境を利用できます。新しい環境を作る場合は、作業フォルダーで次のコマンドを実行します。

```powershell
uv venv
```

PowerShellで仮想環境を有効にします。

```powershell
.venv\Scripts\Activate.ps1
```

必要なパッケージをインストールします。

```powershell
uv pip install Flask Flask-WTF Pillow
```

| パッケージ | 役割 |
| --- | --- |
| Flask | Webアプリ本体 |
| Flask-WTF | CSRF対策 |
| Pillow | 画像データの形式検査 |

---

## 5. フォルダー構成

次の構成でファイルを作ります。

```text
file_app/
├─ app.py
├─ templates/
│  ├─ base.html
│  ├─ upload.html
│  └─ files.html
├─ static/
│  └─ style.css
└─ instance/
   └─ uploads/       ← 起動時に自動作成される
```

アップロードされたファイルは`static`ではなく、`instance/uploads`へ保存します。

`static`のファイルは、通常はURLを知っていればFlaskがそのまま配信します。一方、アップロードファイルを別の場所へ保存し、専用ルートを通して配信すると、ログイン確認や所有者確認などを後から追加しやすくなります。

---

## 6. app.pyを作る

完成版のコードです。あとで部分ごとに読み解きます。

```python
import os
from pathlib import Path
from uuid import uuid4

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_wtf.csrf import CSRFProtect
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename


app = Flask(__name__, instance_relative_config=True)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-before-publishing"),
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
)

csrf = CSRFProtect(app)

UPLOAD_FOLDER = Path(app.instance_path) / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_IMAGE_FORMATS = {
    "PNG": ".png",
    "JPEG": ".jpg",
    "GIF": ".gif",
}


def inspect_image(file):
    """画像を検査し、保存に使う拡張子を返す。"""
    try:
        image = Image.open(file.stream)
        image_format = image.format
        image.verify()
    except (UnidentifiedImageError, OSError, SyntaxError):
        return None
    finally:
        file.stream.seek(0)

    return ALLOWED_IMAGE_FORMATS.get(image_format)


def saved_files():
    """保存済みの通常ファイルを名前順で返す。"""
    return sorted(
        path.name
        for path in app.config["UPLOAD_FOLDER"].iterdir()
        if path.is_file()
    )


@app.get("/")
def index():
    return redirect(url_for("upload_file"))


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("ファイルが送信されていません。", "error")
            return redirect(url_for("upload_file"))

        file = request.files["file"]

        if file.filename == "":
            flash("ファイルを選択してください。", "error")
            return redirect(url_for("upload_file"))

        safe_original_name = secure_filename(file.filename)
        if not safe_original_name:
            flash("ファイル名を確認してください。", "error")
            return redirect(url_for("upload_file"))

        extension = inspect_image(file)
        if extension is None:
            flash("PNG、JPEG、GIF画像だけアップロードできます。", "error")
            return redirect(url_for("upload_file"))

        stored_name = f"{uuid4().hex}{extension}"
        save_path = app.config["UPLOAD_FOLDER"] / stored_name
        file.save(save_path)

        flash("画像をアップロードしました。", "success")
        return redirect(url_for("show_files"))

    return render_template("upload.html")


@app.get("/files")
def show_files():
    return render_template("files.html", files=saved_files())


@app.get("/files/<path:filename>/view")
def view_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
    )


@app.get("/files/<path:filename>/download")
def download_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True,
        download_name=filename,
    )


@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(error):
    return render_template(
        "upload.html",
        error_message="ファイルが大きすぎます。5 MiB以下にしてください。",
    ), 413
```

---

## 7. 設定を読む

### SECRET_KEY

```python
SECRET_KEY=os.environ.get(
    "SECRET_KEY",
    "dev-only-change-before-publishing",
)
```

Flask-WTFのCSRF対策などで利用します。教材用の初期値は開発中だけのものです。公開環境では、予測されにくい値を環境変数`SECRET_KEY`へ設定します。

### MAX_CONTENT_LENGTH

```python
MAX_CONTENT_LENGTH=5 * 1024 * 1024
```

1 KiBは1024バイト、1 MiBは1024 KiBです。この設定では、リクエスト全体をおよそ5 MiBまでに制限します。制限を超えるとFlaskは`413 Request Entity Too Large`エラーを発生させます。

`<input>`の設定だけでは、利用者が制限を回避できます。必ずサーバー側にも容量制限を設定します。

### 保存先

```python
UPLOAD_FOLDER = Path(app.instance_path) / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
```

- `app.instance_path`：設定や実行中に作られるデータを置く場所
- `/ "uploads"`：`pathlib.Path`でパスを結合
- `parents=True`：必要な親フォルダーも作る
- `exist_ok=True`：すでに存在してもエラーにしない

相対パス`"static/uploads"`は、アプリの起動位置によって解釈が変わる可能性があります。ここでは、Flaskが管理する絶対パスを基準にします。

元教材にある`SESSION_TYPE = "filesystem"`はFlask本体の設定ではありません。これは通常、Flask-Sessionなどの拡張機能で使う設定です。今回のファイル保存には必要ありません。

---

## 8. アップロード処理を読む

### 1. フォームからファイルを取得する

```python
if "file" not in request.files:
    # エラー処理

file = request.files["file"]
```

`request.files`には、`multipart/form-data`で送られたファイルが入っています。キーの`"file"`は、HTMLの`name="file"`と一致させます。

### 2. 空のファイル名を確認する

```python
if file.filename == "":
    # エラー処理
```

利用者がファイルを選ばずに送信すると、空のファイル名が届く場合があります。

### 3. ファイル名を安全な形にする

```python
safe_original_name = secure_filename(file.filename)
```

送信されたファイル名は信用できません。たとえば、`../../app.py`のような名前には、意図しない場所のファイルを上書きする危険があります。

`secure_filename()`は、パス区切りなどを取り除き、安全に扱いやすい名前へ変換します。ただし、変換結果が空になることもあるため、結果を確認します。

### 4. ファイルの内容を確認する

```python
extension = inspect_image(file)
```

ファイル名を`photo.jpg`に変えるだけでは、中身がJPEG画像になるわけではありません。`accept="image/*"`や拡張子の確認だけでは不十分です。

この教材ではPillowで画像として読み取り、PNG、JPEG、GIFのいずれかであることを検査します。ただし、1つの検査だけで完全に安全になるわけではありません。公開サービスでは、画像の再エンコード、ピクセル数の制限、マルウェア検査なども検討します。

### 5. 保存名を作る

```python
stored_name = f"{uuid4().hex}{extension}"
```

元のファイル名をそのまま保存すると、同じ名前のファイルが上書きされる可能性があります。そこで、重複しにくいUUIDを保存名に使います。

```text
例：4e987a05f91b42a18a2a4d30d91cf382.png
```

### 6. 保存する

```python
file.save(save_path)
```

検査を通過したファイルだけを保存します。

### 7. リダイレクトする

```python
return redirect(url_for("show_files"))
```

POSTの直後にHTMLを直接返すのではなく、一覧ページへリダイレクトします。これを**Post/Redirect/Get**パターンといい、再読み込みによる二重送信を防ぎやすくなります。

---

## 9. ファイルを表示・ダウンロードする

### send_from_directory

```python
return send_from_directory(
    app.config["UPLOAD_FOLDER"],
    filename,
)
```

`send_from_directory()`は、指定したフォルダー内のファイルをレスポンスとして送ります。利用者がURLへ細工しても保存フォルダーの外側を参照しにくいよう、安全なパス結合を行います。

第1引数の保存フォルダーは、利用者から受け取った値にしてはいけません。アプリ側で決めた信頼できるフォルダーを指定します。

### ブラウザーで表示する

```python
@app.get("/files/<path:filename>/view")
def view_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
    )
```

画像など、ブラウザーが表示できる形式は通常そのまま表示されます。

### ダウンロードさせる

```python
return send_from_directory(
    app.config["UPLOAD_FOLDER"],
    filename,
    as_attachment=True,
    download_name=filename,
)
```

- `as_attachment=True`：添付ファイルとして送る
- `download_name`：保存ダイアログで使う既定のファイル名

ブラウザーの設定によっては、確認画面を出さず既定のダウンロードフォルダーへ保存されます。そのため、必ず「名前を付けて保存」画面が出るとは限りません。

---

## 10. base.htmlを作る

`templates/base.html`を作ります。

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}ファイルアプリ{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <header>
      <nav class="container">
        <a href="{{ url_for('upload_file') }}">アップロード</a>
        <a href="{{ url_for('show_files') }}">ファイル一覧</a>
      </nav>
    </header>

    <main class="container">
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
          <p class="message {{ category }}">{{ message }}</p>
        {% endfor %}
      {% endwith %}

      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

---

## 11. upload.htmlを作る

`templates/upload.html`を作ります。

```html
{% extends "base.html" %}

{% block title %}画像アップロード{% endblock %}

{% block content %}
  <h1>画像をアップロード</h1>
  <p>PNG、JPEG、GIF画像を選んでください。上限は5 MiBです。</p>

  {% if error_message %}
    <p class="message error">{{ error_message }}</p>
  {% endif %}

  <form method="post" enctype="multipart/form-data">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

    <label for="file">画像ファイル</label>
    <input
      type="file"
      id="file"
      name="file"
      accept="image/png,image/jpeg,image/gif"
      required
    >

    <button type="submit">アップロード</button>
  </form>
{% endblock %}
```

### inputの属性

| 属性 | 役割 |
| --- | --- |
| `type="file"` | ファイル選択欄を作る |
| `name="file"` | Flaskで取得するときのキー |
| `accept="..."` | ファイル選択画面で候補を絞る |
| `required` | 未選択のまま送信しにくくする |

`accept`と`required`は利用者の操作を助ける機能です。リクエストは別の方法で作れるため、セキュリティ対策としてはサーバー側の検査も必要です。

`csrf_token`は、別サイトから勝手にPOSTリクエストを送られるCSRF攻撃を防ぐための値です。

---

## 12. files.htmlを作る

`templates/files.html`を作ります。

```html
{% extends "base.html" %}

{% block title %}ファイル一覧{% endblock %}

{% block content %}
  <h1>保存した画像</h1>

  <ul class="file-list">
    {% for filename in files %}
      <li>
        <img
          src="{{ url_for('view_file', filename=filename) }}"
          alt="アップロードされた画像"
        >
        <span>{{ filename }}</span>
        <a href="{{ url_for('download_file', filename=filename) }}">
          ダウンロード
        </a>
      </li>
    {% else %}
      <li>保存された画像はありません。</li>
    {% endfor %}
  </ul>
{% endblock %}
```

`url_for()`へ`filename`を渡すと、次のようなURLが生成されます。

```text
/files/4e987a05f91b42a18a2a4d30d91cf382.png/view
/files/4e987a05f91b42a18a2a4d30d91cf382.png/download
```

---

## 13. CSSを作る

`static/style.css`を作ります。

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

header {
  padding: 1rem 0;
  background: #1d4ed8;
}

nav {
  display: flex;
  gap: 1rem;
}

nav a {
  color: #ffffff;
}

main {
  padding-block: 2rem;
}

form {
  display: grid;
  gap: 1rem;
  max-width: 32rem;
  padding: 1.5rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
}

button {
  width: fit-content;
  padding: 0.6rem 1rem;
  color: #ffffff;
  background: #1d4ed8;
  border: 0;
  border-radius: 0.4rem;
  cursor: pointer;
}

.message {
  padding: 0.75rem;
  border-radius: 0.4rem;
}

.success {
  color: #166534;
  background: #dcfce7;
}

.error {
  color: #991b1b;
  background: #fee2e2;
}

.file-list {
  display: grid;
  gap: 1rem;
  padding: 0;
  list-style: none;
}

.file-list li {
  display: grid;
  grid-template-columns: 120px 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
}

.file-list img {
  width: 120px;
  height: 90px;
  object-fit: cover;
}

@media (max-width: 600px) {
  .file-list li {
    grid-template-columns: 1fr;
  }
}
```

---

## 14. アプリを起動する

```powershell
flask --app app run --debug
```

ブラウザーで次のURLを開きます。

```text
http://127.0.0.1:5000/upload
```

`--debug`は開発中だけ使用します。公開環境ではFlaskの開発サーバーとデバッグモードを使用しません。

---

## 15. 動作を確認する

### 基本機能

- PNG画像をアップロードできる
- JPEG画像をアップロードできる
- GIF画像をアップロードできる
- ファイル一覧に画像が表示される
- ダウンロードリンクから保存できる
- アップロード後に再読み込みしても二重送信されない

### エラー処理

- ファイルを選ばず送信するとメッセージが出る
- テキストファイルを画像名へ変更しても拒否される
- 5 MiBを超えるリクエストが拒否される
- 存在しないファイルのURLは404になる
- `../`を含むURLで保存先の外を参照できない

> セキュリティ確認は、自分が管理する学習環境だけで行います。他人のサービスへ許可なく試してはいけません。

---

## 16. セキュリティ上の注意

ファイルアップロードでは、次の対策を組み合わせます。

| 危険 | 対策例 |
| --- | --- |
| パストラバーサル | `secure_filename()`、UUID、`send_from_directory()` |
| 同名ファイルの上書き | UUIDなどで保存名を生成 |
| 巨大ファイルによる容量消費 | `MAX_CONTENT_LENGTH`、サーバー側の容量監視 |
| 偽の拡張子 | Pillowなどで内容を検査 |
| HTMLやスクリプトによるXSS | 許可形式を限定、公開場所を分離 |
| 他人のファイル閲覧 | ログイン確認、所有者確認 |
| 不正なPOST | CSRFトークン |
| マルウェア | ウイルススキャン、隔離領域、運用監視 |

### 拡張子とMIMEタイプだけを信用しない

ファイル名と`Content-Type`は送信者が変更できます。実際の内容を検査し、用途によっては安全な形式へ再変換します。

### 保存したファイルを実行しない

アップロードフォルダーでは、プログラムを実行できないようにします。画像として受け取ったファイルをPythonコードやHTMLとして実行してはいけません。

### 認証と認可を追加する

この教材のサンプルは、URLを知っている人ならファイルを表示できます。個人用ファイルを扱う場合は、次の処理が必要です。

- ログインしているか確認する
- ファイルの所有者をデータベースへ記録する
- 表示・ダウンロード時に所有者が一致するか確認する

---

## 17. よくあるエラー

### request.filesが空になる

- `<form>`に`enctype="multipart/form-data"`があるか
- `<input>`に`name="file"`があるか
- Flask側も`request.files["file"]`になっているか

### 400 Bad Request / CSRFエラー

POSTフォームに次の隠しフィールドがあるか確認します。

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

### 413 Request Entity Too Large

`MAX_CONTENT_LENGTH`を超えています。画像を小さくするか、用途を考えたうえで上限を変更します。

### 画像が表示されない

- ファイルが`instance/uploads`に保存されているか
- `view_file`のURLを使っているか
- 保存名が一覧の名前と一致しているか
- 画像の読み取り権限があるか

### 同じ画像を選んだのに名前が変わる

上書きとファイル名の衝突を避けるため、アップロードごとにUUIDで新しい保存名を作っています。これは意図した動作です。

---

## 18. 発展課題

- ファイルの削除機能をPOSTで作る
- 元のファイル名、保存名、投稿者をデータベースへ記録する
- ログインした本人だけが自分のファイルを閲覧できるようにする
- 画像の縦横サイズとピクセル数に上限を付ける
- 画像を安全な形式へ再エンコードする
- サムネイル画像を自動生成する
- アップロード日時を一覧へ表示する
- クラウドストレージへ保存する構成を調べる

---

## 19. 確認問題

### 問題1

ファイルを送る`form`に必要な`enctype`を書いてください。

<details>
<summary>解答</summary>

```html
enctype="multipart/form-data"
```

</details>

### 問題2

`accept="image/png"`を付ければ、サーバー側のファイル検査は不要でしょうか。

<details>
<summary>解答</summary>

不要にはなりません。`accept`はファイル選択を助ける機能であり、リクエストは書き換えられます。サーバー側でも検査します。

</details>

### 問題3

ダウンロードとしてファイルを送るとき、`send_from_directory()`へ指定するオプションは何でしょうか。

<details>
<summary>解答</summary>

```python
as_attachment=True
```

</details>

### 問題4

アップロード後に一覧ページへリダイレクトする理由を説明してください。

<details>
<summary>解答例</summary>

Post/Redirect/Getパターンにして、ページの再読み込みによるファイルの二重送信を防ぎやすくするためです。

</details>

---

## 20. まとめ

- ファイル送信フォームには`multipart/form-data`を指定する
- Flaskでは`request.files`からファイルを取得する
- ファイル名、内容、容量をサーバー側で検査する
- 保存名はUUIDなどで作り、衝突や危険なパスを避ける
- アップロードファイルは`static`から分離すると管理しやすい
- `send_from_directory()`で保存フォルダー内のファイルを送れる
- `as_attachment=True`でダウンロードとして送信できる
- 公開サービスでは認証、認可、マルウェア検査なども必要になる

---

## 参考資料

### 元教材

- [Flaskでのファイルのアップロードとダウンロード](https://app.notion.com/p/323b4d03741180c4b830d8d2f1f4bf45)

### 公式資料

- [Flask公式ドキュメント：Uploading Files](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
- [Flask公式API：send_from_directory](https://flask.palletsprojects.com/en/stable/api/#flask.send_from_directory)
- [Flask公式ドキュメント：Security Considerations](https://flask.palletsprojects.com/en/stable/web-security/)
