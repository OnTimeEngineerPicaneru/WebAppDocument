# FlaskとJavaScriptでモーダル画面を作る

この資料では、HTMLの`<dialog>`要素でモーダル画面を開き、入力されたデータをJavaScriptのFetch APIでFlaskへ送信する方法を解説します。

モーダル画面とは、現在のページの上に重ねて表示される小さな画面です。モーダル画面を閉じるまで背後のページを操作できないため、入力、確認、警告など、利用者の注意を一時的に集めたい場面で使われます。

---

## 1. アプリ全体の流れ

```text
「入力する」ボタンを押す
        ↓
<dialog>をモーダル表示する
        ↓
利用者が文字を入力する
        ↓
JavaScriptがJSONへ変換する
        ↓
Fetch APIでFlaskへPOSTする
        ↓
FlaskがJSONを検証して処理する
        ↓
FlaskがJSONで結果を返す
        ↓
ページ内へ結果を表示し、モーダルを閉じる
```

このアプリでは、次の技術が協力して動きます。

| 技術 | 役割 |
| --- | --- |
| HTML | ページとモーダル画面の構造 |
| CSS | モーダル画面や背景の見た目 |
| JavaScript | 開閉操作、データ送信、結果表示 |
| Flask | 入力の検証とJSONレスポンス |
| HTTP | ブラウザーとFlaskの通信 |

---

## 2. フォルダー構成

```text
modal_app/
├─ app.py
├─ templates/
│  └─ index.html
└─ static/
   ├─ style.css
   └─ modal.js
```

JavaScriptをHTMLへ直接書くこともできますが、役割を分けて読みやすくするため、`static/modal.js`へ保存します。

Flask-WTFを使ってCSRF対策を行うため、必要なパッケージをインストールします。

```powershell
uv pip install Flask Flask-WTF
```

---

## 3. app.pyを作る

```python
import os

from flask import Flask, jsonify, render_template, request
from flask_wtf.csrf import CSRFError, CSRFProtect


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-before-publishing",
)

csrf = CSRFProtect(app)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/submit")
def submit():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            status="error",
            message="正しいJSONを送信してください。",
        ), 400

    value = data.get("value")

    if not isinstance(value, str):
        return jsonify(
            status="error",
            message="文字列を入力してください。",
        ), 400

    value = value.strip()

    if not value:
        return jsonify(
            status="error",
            message="入力内容が空です。",
        ), 400

    if len(value) > 100:
        return jsonify(
            status="error",
            message="入力内容は100文字以内にしてください。",
        ), 400

    app.logger.info("モーダル画面からデータを受信しました。")

    return jsonify(
        status="success",
        message=f"サーバーで「{value}」を受け取りました。",
    )


@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    return jsonify(
        status="error",
        message="送信の有効期限が切れました。ページを再読み込みしてください。",
    ), 400
```

### GETとPOSTを分ける

```python
@app.get("/")
def index():
```

`GET /`はHTMLページを返します。

```python
@app.post("/submit")
def submit():
```

`POST /submit`はJavaScriptからJSONを受け取り、処理結果をJSONで返します。Flaskでは`@app.post()`を使うと、POSTだけを受け付けるルートを簡潔に書けます。

### JSONを受け取る

```python
data = request.get_json(silent=True)
```

`request.get_json()`は、リクエスト本文のJSONをPythonの値へ変換します。今回送るJSONオブジェクトは、Pythonでは辞書になります。

```text
JSON                         Python
{"value": "こんにちは"}  →  {"value": "こんにちは"}
```

`silent=True`を指定すると、JSONとして解析できない場合に例外レスポンスを自動生成せず、`None`を返します。その後のコードで、アプリに合ったエラーメッセージを返します。

### 入力値を検証する

ブラウザーから送られたデータは信用せず、サーバー側で確認します。

```python
if not isinstance(data, dict):
    # JSONオブジェクトでなければ400を返す

if not isinstance(value, str):
    # valueが文字列でなければ400を返す

value = value.strip()

if not value:
    # 空文字なら400を返す

if len(value) > 100:
    # 100文字を超えたら400を返す
```

JavaScript側にも入力チェックを作りますが、リクエストは開発者ツールや別のプログラムから変更できます。そのため、Flask側の検証を省略してはいけません。

### JSONを返す

```python
return jsonify(
    status="success",
    message=f"サーバーで「{value}」を受け取りました。",
)
```

`jsonify()`はPythonの値をJSONレスポンスへ変換し、適切な`Content-Type`を設定します。

エラーの場合は、レスポンスの後ろにHTTPステータスコード`400`を付けています。

```python
return jsonify(
    status="error",
    message="入力内容が空です。",
), 400
```

---

## 4. index.htmlを作る

`templates/index.html`を作ります。

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>Flaskモーダル送信</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="{{ url_for('static', filename='modal.js') }}" defer></script>
  </head>
  <body>
    <main class="container">
      <h1>Flaskモーダル送信</h1>
      <p>モーダル画面に入力した文字をFlaskへ送信します。</p>

      <button type="button" id="open-button">
        入力する
      </button>

      <p id="result" class="result" role="status" aria-live="polite"></p>
    </main>

    <dialog id="input-dialog" aria-labelledby="dialog-title">
      <form id="input-form">
        <h2 id="dialog-title">値を入力してください</h2>

        <label for="user-input">送信する文字</label>
        <input
          type="text"
          id="user-input"
          name="value"
          maxlength="100"
          autocomplete="off"
          required
          autofocus
        >

        <p id="dialog-error" class="error" role="alert"></p>

        <div class="buttons">
          <button type="submit" id="send-button">
            Flaskへ送信
          </button>
          <button type="button" id="close-button" class="secondary">
            閉じる
          </button>
        </div>
      </form>
    </dialog>
  </body>
</html>
```

### dialog要素

```html
<dialog id="input-dialog" aria-labelledby="dialog-title">
  ...
</dialog>
```

`<dialog>`は、ダイアログやモーダル画面を表すHTML要素です。ページを開いた時点では非表示です。

`aria-labelledby="dialog-title"`によって、`id="dialog-title"`を持つ見出しがダイアログの名前であることを支援技術へ伝えます。

`showModal()`で開いた`<dialog>`は、ブラウザーによってモーダルとして扱われます。背後のページは操作できなくなり、通常はEscキーでも閉じられます。

### 閉じる手段を用意する

```html
<button type="button" id="close-button">閉じる</button>
```

マウス、タッチ、キーボードなど、利用方法に関係なく閉じられるよう、ダイアログ内に明確な閉じるボタンを用意します。

### autofocus

```html
<input ... autofocus>
```

モーダルを開いたとき、入力欄へフォーカスを移します。利用者がすぐ入力を始められ、キーボード操作もしやすくなります。

### role=statusとaria-live

```html
<p id="result" role="status" aria-live="polite"></p>
```

JavaScriptが後から追加した結果を、スクリーンリーダーなどが利用者へ伝えられるようにします。

---

## 5. CSSを作る

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
  padding-block: 3rem;
}

button {
  padding: 0.7rem 1rem;
  color: #ffffff;
  font: inherit;
  background: #1d4ed8;
  border: 0;
  border-radius: 0.4rem;
  cursor: pointer;
}

button:disabled {
  cursor: wait;
  opacity: 0.6;
}

button.secondary {
  color: #1f2937;
  background: #e2e8f0;
}

dialog {
  width: min(90%, 480px);
  padding: 1.5rem;
  border: 0;
  border-radius: 0.75rem;
  box-shadow: 0 1rem 3rem rgb(0 0 0 / 25%);
}

dialog::backdrop {
  background: rgb(0 0 0 / 55%);
}

form {
  display: grid;
  gap: 1rem;
}

input {
  width: 100%;
  padding: 0.7rem;
  font: inherit;
  border: 1px solid #94a3b8;
  border-radius: 0.4rem;
}

.buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.result {
  min-height: 1.5rem;
  color: #166534;
}

.error {
  min-height: 1.5rem;
  margin: 0;
  color: #b91c1c;
}
```

### ::backdrop

```css
dialog::backdrop {
  background: rgb(0 0 0 / 55%);
}
```

`::backdrop`は、`showModal()`で開いたダイアログの背後に表示される領域を選択します。この例では半透明の黒色を付け、モーダル画面を目立たせています。

---

## 6. JavaScriptを作る

`static/modal.js`を作ります。

```javascript
const dialog = document.getElementById("input-dialog");
const form = document.getElementById("input-form");
const openButton = document.getElementById("open-button");
const closeButton = document.getElementById("close-button");
const sendButton = document.getElementById("send-button");
const userInput = document.getElementById("user-input");
const dialogError = document.getElementById("dialog-error");
const result = document.getElementById("result");
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");


openButton.addEventListener("click", () => {
  dialogError.textContent = "";
  dialog.showModal();
});


closeButton.addEventListener("click", () => {
  dialog.close();
});


form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const value = userInput.value.trim();

  if (!value) {
    dialogError.textContent = "文字を入力してください。";
    userInput.focus();
    return;
  }

  sendButton.disabled = true;
  dialogError.textContent = "";

  try {
    const response = await fetch("/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ value }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "送信に失敗しました。");
    }

    result.textContent = data.message;
    form.reset();
    dialog.close();
  } catch (error) {
    console.error(error);
    dialogError.textContent = error.message;
  } finally {
    sendButton.disabled = false;
  }
});
```

---

## 7. HTML要素を取得する

```javascript
const dialog = document.getElementById("input-dialog");
```

`document.getElementById()`は、指定した`id`を持つHTML要素を取得します。取得した要素を変数へ保存すると、イベントの登録や内容の変更に使えます。

```text
HTML                              JavaScript
id="input-dialog"       ←→       dialog
id="open-button"        ←→       openButton
id="user-input"         ←→       userInput
```

HTMLの`id`とJavaScriptの文字列が一致していない場合、要素を取得できず`null`になります。

---

## 8. イベントリスナー

```javascript
openButton.addEventListener("click", () => {
  dialog.showModal();
});
```

`addEventListener()`は、指定したイベントが発生したときに実行する処理を登録します。

| 部分 | 意味 |
| --- | --- |
| `openButton` | イベントを監視する要素 |
| `"click"` | クリックイベント |
| `() => { ... }` | イベント発生時に実行する関数 |

### アロー関数

`() => { ... }`は、関数を書く方法の1つです。

```javascript
function openDialog() {
  dialog.showModal();
}
```

```javascript
const openDialog = () => {
  dialog.showModal();
};
```

細かな動作がすべて同じとは限りませんが、このイベント処理ではどちらの形でも関数を登録できます。

### formのsubmitを監視する

```javascript
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  // 送信処理
});
```

送信ボタンの`click`ではなく、フォームの`submit`を監視しています。これにより、入力欄でEnterキーを押した場合も同じ処理を実行できます。

`event.preventDefault()`は、フォーム本来のページ移動を止め、Fetch APIによる送信へ切り替えます。

---

## 9. showModalとclose

```javascript
dialog.showModal();
```

`showModal()`は`<dialog>`をモーダル表示します。背後のページは操作できなくなります。

```javascript
dialog.close();
```

`close()`はダイアログを閉じます。このサンプルでは次の場合に呼び出します。

- 「閉じる」ボタンを押したとき
- Flaskへの送信が成功したとき

入力エラーや通信エラーの場合は閉じず、モーダル内へエラーメッセージを表示します。利用者が入力を直して再送信できるためです。

---

## 10. asyncとawait

Fetch APIは、サーバーの応答を待つ**非同期処理**です。

```javascript
form.addEventListener("submit", async (event) => {
  const response = await fetch(...);
  const data = await response.json();
});
```

- `async`：関数内で`await`を使えるようにする
- `await`：Promiseの結果が得られるまで、その関数内の続きの処理を待つ

通信を待っている間も、ブラウザー全体が停止するわけではありません。

元教材で使われていた`.then()`でも同じ通信を書けます。

```javascript
fetch("/submit", options)
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.error(error);
  });
```

この教材では、処理の順序を上から読みやすい`async`と`await`を使用しています。

---

## 11. Fetch APIでJSONを送る

```javascript
const response = await fetch("/submit", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken,
  },
  body: JSON.stringify({ value }),
});
```

| 設定 | 役割 |
| --- | --- |
| `"/submit"` | Flaskの送信先URL |
| `method: "POST"` | HTTPメソッドをPOSTにする |
| `Content-Type` | 本文がJSONであることを伝える |
| `X-CSRFToken` | CSRF対策用のトークンを送る |
| `body` | リクエスト本文 |

### JSON.stringify

```javascript
JSON.stringify({ value })
```

これはプロパティ名と変数名が同じ場合の省略記法です。

```javascript
JSON.stringify({ value: value })
```

JavaScriptオブジェクトを、通信で送れるJSON文字列へ変換します。

```text
JavaScriptオブジェクト          JSON文字列
{ value: "こんにちは" }   →   '{"value":"こんにちは"}'
```

---

## 12. レスポンスを処理する

```javascript
const data = await response.json();
```

`response.json()`は、レスポンス本文のJSONをJavaScriptの値へ変換します。この処理も非同期のため`await`を付けます。

### response.okを確認する

```javascript
if (!response.ok) {
  throw new Error(data.message || "送信に失敗しました。");
}
```

Fetch APIは、ネットワークへ接続できない場合などには失敗しますが、サーバーが`400`や`500`を返しただけでは自動的に`catch`へ移動しません。

`response.ok`は、HTTPステータスコードが200から299の範囲なら`true`になります。必ず確認して、エラーレスポンスを成功として扱わないようにします。

### textContentで表示する

```javascript
result.textContent = data.message;
```

受け取った文字列は`innerHTML`ではなく`textContent`で表示します。文字列中のHTMLタグを実行せず、そのまま文字として表示できるため安全です。

---

## 13. try、catch、finally

```javascript
try {
  // 通信と成功時の処理
} catch (error) {
  // 通信失敗やHTTPエラーの処理
} finally {
  // 成功・失敗にかかわらず行う処理
}
```

このサンプルでは、送信中にボタンを無効にし、処理が終わったら再び有効にします。

```javascript
sendButton.disabled = true;

try {
  // 送信処理
} finally {
  sendButton.disabled = false;
}
```

二重クリックによる連続送信を防ぎやすくなります。ただし、重要な登録処理ではサーバー側でも二重登録への対策が必要です。

---

## 14. JavaScriptとFlaskの対応

| ブラウザー側 | Flask側 |
| --- | --- |
| `fetch("/submit")` | `@app.post("/submit")` |
| `Content-Type: application/json` | `request.get_json()` |
| `JSON.stringify({ value })` | `data.get("value")` |
| `X-CSRFToken` | `CSRFProtect(app)` |
| `response.json()` | `jsonify(...)` |
| `response.ok` | HTTPステータスコード |

送信データの例：

```json
{
  "value": "こんにちは"
}
```

成功レスポンスの例：

```json
{
  "status": "success",
  "message": "サーバーで「こんにちは」を受け取りました。"
}
```

入力エラーレスポンスの例：

```json
{
  "status": "error",
  "message": "入力内容が空です。"
}
```

エラーの場合は、JSONだけでなく`400 Bad Request`などのHTTPステータスコードも返します。

---

## 15. CSRF対策

ログイン状態やCookieを利用するWebアプリでは、別のサイトから利用者の意図しないPOSTを送られる可能性があります。これをCSRFといいます。

Flask-WTFの`CSRFProtect`を設定し、HTMLへトークンを埋め込みます。

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

JavaScriptで値を取得します。

```javascript
const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
```

Fetch APIのリクエストヘッダーで送ります。

```javascript
headers: {
  "Content-Type": "application/json",
  "X-CSRFToken": csrfToken,
}
```

CSRF対策は、入力値検証やXSS対策とは目的が異なります。それぞれを組み合わせます。

---

## 16. エラーが起きたときの確認

### モーダルが開かない

- HTMLとJavaScriptの`id`が一致しているか
- `modal.js`を読み込めているか
- ブラウザーのコンソールにエラーがないか
- `dialog.showModal()`の対象が`<dialog>`要素か

### 送信するとページが移動する

フォームの`submit`イベント内で、次の処理を実行しているか確認します。

```javascript
event.preventDefault();
```

### 400 Bad Requestになる

- `Content-Type`が`application/json`か
- `body`を`JSON.stringify()`しているか
- `X-CSRFToken`を送っているか
- `value`が文字列で、空になっていないか

### 404 Not Foundになる

JavaScriptの送信先`/submit`と、Flaskの`@app.post("/submit")`が一致しているか確認します。

### 405 Method Not Allowedになる

Flask側はPOSTだけを受け付けます。Fetch APIに`method: "POST"`があるか確認します。

### catchが実行されない

`fetch()`は404や500を受け取っただけではPromiseを拒否しません。`response.ok`を確認し、必要に応じて`throw`します。

### JSONの読み取りでエラーになる

FlaskがHTMLのエラーページを返している可能性があります。開発者ツールのNetworkタブで、ステータスコード、`Content-Type`、レスポンス本文を確認します。

---

## 17. セキュリティと設計上の注意

- ブラウザー側だけでなくFlask側でも入力を検証する
- データベースへ保存する場合は文字数や形式を制限する
- 認証が必要な処理にはログイン確認を追加する
- 他人のデータを更新できないよう所有者を確認する
- 更新・削除処理ではCSRF対策を行う
- 受信値をログへそのまま残す場合は個人情報に注意する
- HTMLへ文字列を出すときは`textContent`やJinjaの自動エスケープを利用する
- 公開環境ではFlaskのデバッグモードを使わない

モーダル画面は見た目を変える仕組みであり、アクセス制御や入力値検証の代わりにはなりません。重要な判断は必ずサーバー側で行います。

---

## まとめ

- `<dialog>`はブラウザー標準のダイアログ要素
- `showModal()`で開き、`close()`で閉じる
- `::backdrop`でモーダル背後の見た目を設定できる
- `addEventListener()`でクリックやフォーム送信の処理を登録する
- Fetch APIを使うと、ページを再読み込みせずFlaskと通信できる
- `JSON.stringify()`でJavaScriptの値をJSON文字列へ変換する
- Flaskでは`request.get_json()`で受け取り、`jsonify()`で返す
- `fetch()`では`response.ok`を自分で確認する
- 入力検証、CSRF対策、エラー処理はサーバー側にも必要
- モーダル内には見出し、閉じるボタン、適切なフォーカス先を用意する

---

## 参考資料

### 元教材

- [HTMLのポップアップ画面とFlaskでの処理](https://app.notion.com/p/347b4d03741180b58038d907689a282f)

### 公式・技術資料

- [MDN：dialog要素](https://developer.mozilla.org/ja/docs/Web/HTML/Reference/Elements/dialog)
- [MDN：Fetch APIの使用](https://developer.mozilla.org/ja/docs/Web/API/Fetch_API/Using_Fetch)
- [Flask公式ドキュメント：Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Flask-WTF公式ドキュメント：CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf/)
