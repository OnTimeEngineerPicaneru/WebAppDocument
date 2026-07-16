# Webアプリ作成講座

中学生を対象とした、Webアプリ開発の学習用リポジトリです。

Webページの仕組み、HTML、CSS、ネットワーク、Python、Flask、データベース、JavaScriptなどを段階的に学び、最終的にログイン機能を備えたTodoアプリを作成します。

## リポジトリの構成

```text
Webアプリ作成講座/
├─ README.md          # このリポジトリの説明
├─ 授業資料/           # 配布用のMarkdown教材
└─ ToDoApplication/   # Flaskで作成したTodoアプリ
```

## 授業資料

教材は[授業資料](./授業資料/)フォルダーに収録しています。

| 番号 | 教材 | おもな内容 |
| --- | --- | --- |
| 01 | [Webページの基礎知識](./授業資料/01_Webページの基礎知識.md) | Webサイト、ブラウザー、サーバー、URL |
| 02 | [Webページ制作の流れ](./授業資料/02_Webページ制作の流れ.md) | 企画から公開までの制作工程 |
| 03 | [HTMLのまとめ](./授業資料/03_HTMLのまとめ.md) | HTMLの文法とページ構造 |
| 04 | [CSSのまとめ](./授業資料/04_CSSのまとめ.md) | 装飾、レイアウト、レスポンシブ対応 |
| 05 | [ネットワーク基礎知識](./授業資料/05_ネットワーク基礎知識.md) | IPアドレス、DNS、HTTP、HTTPS |
| 06 | [FlaskでTodoアプリを作成](./授業資料/06_FlaskでTodoアプリを作成.md) | Flask、認証、データベース、CRUD |
| 07 | [Flaskでのテンプレートエンジン](./授業資料/07_Flaskでのテンプレートエンジン.md) | Jinja、テンプレート継承、変数、繰り返し |
| 08 | [Bootstrapドキュメント](./授業資料/08_Bootstrapドキュメント.md) | Bootstrapによる画面デザイン |
| 09 | [Flaskでのファイルのアップロードとダウンロード](./授業資料/09_Flaskでのファイルのアップロードとダウンロード.md) | ファイル送受信と安全な保存 |
| 10 | [Pythonの例外処理](./授業資料/10_Pythonの例外処理.md) | `try`、`except`、`raise`、独自例外 |
| 11 | [FlaskとJavaScriptでモーダル画面を作る](./授業資料/11_FlaskとJavaScriptでモーダル画面を作る.md) | `<dialog>`、Fetch API、JSON通信 |

基本的には、番号の小さい教材から順番に読み進めます。Pythonの基本文法を学習済みの場合は、Webの基礎を確認したあと、Flaskの教材へ進むこともできます。

## サンプルアプリ

[ToDoApplication](./ToDoApplication/)は、教材で扱う技術を組み合わせたFlask製Todoアプリです。

次の機能を実装しています。

- ユーザー登録
- ログイン・ログアウト
- ユーザーごとのタスク一覧
- タスクの登録・編集・削除
- 4種類のタスクステータス
- パスワードのハッシュ化
- CSRF対策
- 入力値の検証
- SQLiteによるデータ保存
- Bootstrapによる画面デザイン

詳しい構成と操作方法は、[ToDoApplicationのREADME](./ToDoApplication/README.md)を参照してください。

## サンプルアプリの起動

### 1. アプリのフォルダーへ移動する

```powershell
cd ToDoApplication
```

### 2. 仮想環境を作る

```powershell
python -m venv .venv
```

### 3. 仮想環境を有効にする

PowerShellの場合：

```powershell
.venv\Scripts\Activate.ps1
```

macOSまたはLinuxの場合：

```bash
source .venv/bin/activate
```

### 4. 必要なパッケージをインストールする

```powershell
python -m pip install -r requirements.txt
```

### 5. 環境変数ファイルを作る

PowerShellの場合：

```powershell
Copy-Item .env.example .env
```

macOSまたはLinuxの場合：

```bash
cp .env.example .env
```

`.env`の`SECRET_KEY`は、自分用の予測されにくい値へ変更してください。`.env`はGitの管理対象外です。

### 6. データベースを準備する

```powershell
flask --app app db upgrade
```

### 7. 開発サーバーを起動する

```powershell
flask --app app run --debug
```

ブラウザーで次のURLを開きます。

```text
http://127.0.0.1:5000/
```

`--debug`は開発中だけ使用してください。インターネットへ公開する環境では、Flaskの開発サーバーを使用しません。

## おもな使用技術

| 分類 | 技術 |
| --- | --- |
| 言語 | Python、HTML、CSS、JavaScript |
| Webフレームワーク | Flask |
| テンプレートエンジン | Jinja |
| ORM | Flask-SQLAlchemy |
| マイグレーション | Flask-Migrate |
| 認証 | Flask-Login |
| CSRF対策 | Flask-WTF |
| データベース | SQLite |
| CSSフレームワーク | Bootstrap 5 |

## 取り扱い上の注意

- 教材内のサンプルコードは、学習しやすさを優先した小さな構成です。
- パスワード、秘密鍵、個人情報をGitへ登録しないでください。
- 公開環境ではHTTPS、本番用WSGIサーバー、適切なログ管理などが必要です。
- 外部サービスや他人のシステムに対し、許可なくセキュリティテストを行わないでください。
- ライブラリの仕様は更新されるため、実際の開発では公式ドキュメントも確認してください。

## ライセンスと利用範囲

授業外での配布、改変、公開を行う場合は、リポジトリ管理者が定める利用条件を確認してください。外部ライブラリや引用資料には、それぞれのライセンスと利用条件が適用されます。
