# トラブルシューティング

## flaskコマンドが見つからない

仮想環境が有効になっているか確認します。

PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

パッケージを再インストールします。

```bash
python -m pip install -r requirements.txt
```

## ModuleNotFoundError

表示されたモジュールが、現在使用しているPython環境に入っていません。

```bash
python -m pip install -r requirements.txt
```

エディターが別のPythonを選んでいないかも確認します。

## データベースのテーブルがない

マイグレーションを適用します。

```bash
flask --app app db upgrade
```

## 400 Bad Request / CSRFエラー

- POSTフォームに`csrf_token`があるか
- ページを長時間開いたままにしていないか
- `.env`の`SECRET_KEY`が起動ごとに変わっていないか

ページを再読み込みしてから、もう一度送信します。

## 404 Not Found

- URLのスペルを確認する
- `@app.route()`、`@app.get()`、`@app.post()`のパスを確認する
- `url_for()`へ正しい関数名を指定しているか確認する

## 405 Method Not Allowed

URLは存在しますが、GETとPOSTが一致していません。フォームの`method`とFlaskルートが対応しているか確認します。

## タスクの重複エラー

同じユーザーは、同じ名前のタスクを複数登録できません。別のタスク名を入力します。

## Bootstrapの閉じるボタンが動かない

BootstrapのJavaScript Bundleを読み込んでいるか確認します。

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

## CSSが反映されない

- CSSファイルを`static`フォルダーへ置く
- `url_for('static', filename='...')`で読み込む
- ブラウザーのキャッシュを更新する

## 解決しない場合

次の情報を確認すると原因を調べやすくなります。

- 表示されたエラーメッセージ
- トレースバックの最後の行
- 問題が発生したURLと操作
- ターミナルの出力
- ブラウザー開発者ツールのConsoleとNetwork

秘密鍵、パスワード、個人情報は質問文やスクリーンショットへ含めないでください。
