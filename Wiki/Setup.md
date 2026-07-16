# 開発環境のセットアップ

## 必要なもの

- Python 3
- Git
- Webブラウザー
- Visual Studio Codeなどのエディター

## リポジトリを取得する

```bash
git clone https://github.com/OnTimeEngineerPicaneru/WebAppDocument.git
cd WebAppDocument/ToDoApplication
```

## 仮想環境を作る

```bash
python -m venv .venv
```

PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

macOSまたはLinux：

```bash
source .venv/bin/activate
```

## パッケージをインストールする

```bash
python -m pip install -r requirements.txt
```

## 環境変数を設定する

PowerShell：

```powershell
Copy-Item .env.example .env
```

macOSまたはLinux：

```bash
cp .env.example .env
```

`.env`の`SECRET_KEY`を自分用のランダムな値へ変更します。

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

`.env`には秘密情報が含まれるため、GitHubへ登録しません。

## データベースを準備する

```bash
flask --app app db upgrade
```

## 開発サーバーを起動する

```bash
flask --app app run --debug
```

ブラウザーで次のURLを開きます。

```text
http://127.0.0.1:5000/
```

`--debug`は開発環境だけで使用します。

## 終了する

ターミナルで`Ctrl+C`を押すとサーバーが停止します。仮想環境を終了する場合は次を実行します。

```bash
deactivate
```

## 関連ページ

- [[トラブルシューティング|Troubleshooting]]
- [[セキュリティ上の注意|Security]]
