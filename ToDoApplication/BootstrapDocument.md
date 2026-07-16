このドキュメントでは、ToDoアプリケーションで使用されているBootstrap 5の各機能について、実際のコード例を用いて解説します。


## Bootstrapとは

Bootstrapは、レスポンシブでモバイルフレンドリーなWebサイトを素早く構築できる、世界で最も人気のあるCSSフレームワークです。

### 主な特徴
- **レスポンシブデザイン**: 画面サイズに応じて自動的にレイアウトが調整される
- **豊富なコンポーネント**: ボタン、フォーム、ナビゲーションなどすぐに使えるパーツが多数
- **カスタマイズ可能**: 色やサイズを簡単に変更できる

---

## 導入方法

### CDN経由で読み込む方法

このプロジェクトでは、CDN（Content Delivery Network）を使用してBootstrapを読み込んでいます。

```html
<head>
    <meta charset="UTF-8" />
    <title>ログイン - Todoアプリ</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
```

**解説:**
- `<link>` タグで外部のCSSファイルを読み込む
- `href` 属性にBootstrap 5.3.0のCDN URLを指定
- これだけで、すべてのBootstrapのスタイルが利用可能になる

---

## レイアウトシステム

Bootstrapのレイアウトシステムは、**コンテナ**、**行（Row）**、**列（Column）** の3つの要素で構成されています。

### 1. コンテナ (Container)

#### login.html の例

```html
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <!-- コンテンツ -->
        </div>
    </div>
</div>
```

**解説:**
- `container`: コンテンツを中央に配置し、左右に余白を作る
- `mt-5`: Margin Top（上部の余白）を5段階分追加
- レスポンシブに画面幅に応じて自動調整される

### 2. 行と列 (Row & Column)

#### home.html の例

```html
<div class="row justify-content-center">
    <div class="col-md-6">
        <!-- ログインフォーム -->
    </div>
</div>
```

**解説:**
- `row`: 横並びのレイアウトを作成
- `justify-content-center`: 子要素を水平方向の中央に配置
- `col-md-6`: 中型画面（md）以上で12分割のうち6列分（50%）の幅を使用

### グリッドシステムの仕組み

Bootstrapは画面を**12分割**して考えます：

| クラス | 幅 |
|--------|-----|
| `col-md-12` | 100% (12/12) |
| `col-md-6` | 50% (6/12) |
| `col-md-4` | 33.3% (4/12) |
| `col-md-8` | 66.6% (8/12) |

#### register.html の例

```html
<div class="col-md-8">
    <!-- 登録フォーム -->
</div>
```

**解説:**
- `col-md-8`: 中型画面以上で66.6%の幅を使用
- ログイン画面（50%）より少し広めに設定

---

## カード (Card)

カードは、内容をボックスで囲んで見やすく表示するコンポーネントです。

### 基本構造

#### login.html の例

```html
<div class="card">
    <div class="card-header bg-primary text-white">
        <h4>ログイン</h4>
    </div>
    <div class="card-body">
        <!-- フォームの内容 -->
    </div>
</div>
```

**解説:**

1. **カード全体** (`card`)
   - 枠線と影がついたボックスを作成

2. **カードヘッダー** (`card-header`)
   - カードの上部にタイトルを表示
   - `bg-primary`: 背景色を青色に設定
   - `text-white`: 文字色を白色に設定

3. **カードボディ** (`card-body`)
   - カードのメインコンテンツ部分
   - 内側に自動的に余白が追加される

### 色の種類

#### add_task.html の例

```html
<div class="card-header bg-success text-white">
    <h4>新しいタスクの作成</h4>
</div>
```

#### edit_task.html の例

```html
<div class="card-header bg-primary text-white">
    <h4>タスクの編集</h4>
</div>
```

**利用可能な背景色:**

| クラス | 色 | 用途 |
|--------|-----|------|
| `bg-primary` | 青 | 主要な操作 |
| `bg-success` | 緑 | 成功・作成 |
| `bg-danger` | 赤 | 削除・エラー |
| `bg-warning` | 黄色 | 警告 |
| `bg-info` | 水色 | 情報 |
| `bg-secondary` | グレー | 副次的な要素 |
| `bg-dark` | 黒 | ヘッダーなど |

---

## フォーム (Form)

Bootstrapは、美しく使いやすいフォームを簡単に作成できます。

### 基本的なフォーム要素

#### login.html の例

```html
<form action="{{ url_for('login') }}" method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
    <div class="mb-3">
        <label for="login_id" class="form-label">ログインID</label>
        <input
            type="text"
            class="form-control"
            name="login_id"
            placeholder="IDを入力してください"
            required
        />
    </div>

    <div class="mb-3">
        <label for="password" class="form-label">パスワード</label>
        <input
            type="password"
            class="form-control"
            name="password"
            placeholder="パスワードを入力"
            required
        />
    </div>
</form>
```

**解説:**

1. **フォームグループ** (`mb-3`)
   - `mb-3`: Margin Bottom（下の余白）を3段階分追加
   - 各入力項目の間隔を作る

2. **ラベル** (`form-label`)
   - 入力欄の説明テキスト
   - 適切なフォントサイズと余白が設定される

3. **入力欄** (`form-control`)
   - テキストボックスにBootstrapのスタイルを適用
   - 枠線、パディング、フォーカス時の効果などが自動設定される

### セレクトボックス

#### add_task.html の例

```html
<div class="mb-3">
    <label for="status" class="form-label">状態</label>
    <select class="form-select" name="status">
        <option value="NOT_STARTED">未達成</option>
        <option value="IN_PROGRESS">進行中</option>
        <option value="COMPLETED">実施済み</option>
        <option value="PENDING">保留中</option>
    </select>
</div>
```

**解説:**
- `form-select`: セレクトボックス用のスタイル
- `form-control` と同様のデザインで統一感を維持

### 選択状態の設定

#### edit_task.html の例

```html
<select class="form-select" name="status">
    <option value="NOT_STARTED" {% if task.status.name == "NOT_STARTED" %}selected{% endif %}>未達成</option>
    <option value="IN_PROGRESS" {% if task.status.name == "IN_PROGRESS" %}selected{% endif %}>進行中</option>
    <option value="COMPLETED" {% if task.status.name == "COMPLETED" %}selected{% endif %}>実施済み</option>
    <option value="PENDING" {% if task.status.name == "PENDING" %}selected{% endif %}>保留中</option>
</select>
```

**解説:**
- Jinjaテンプレートで条件分岐
- 現在の値と一致するオプションに `selected` 属性を追加
- 編集画面で現在の値が選択された状態で表示される

### 入力欄に値を設定

#### edit_task.html の例

```html
<input
    type="text"
    class="form-control"
    name="task_name"
    value="{{ task.task_name }}"
    placeholder="例:漢字ドリル"
    required
/>
```

**解説:**
- `value="{{ task.task_name }}"`: データベースから取得した値を表示
- 編集画面で既存の値が入力された状態になる

### 無効化された入力欄

#### edit_task.html の例

```html
<div class="mb-3">
    <label class="form-label">作成日時</label>
    <input type="text" class="form-control" value="{{ task.time_stamp }}" disabled />
    <small class="text-muted">作成日時は変更できません</small>
</div>
```

**解説:**
- `disabled`: 入力欄を無効化（読み取り専用）
- グレーアウトされて編集不可であることを示す
- `text-muted`: 補足テキストを薄い色で表示

### ヘルプテキスト

#### register.html の例

```html
<div class="mb-3">
    <label for="login_id" class="form-label">ログインID</label>
    <input type="text" class="form-control" name="login_id" id="login_id"
        placeholder="例：root" required />
    <div class="form-text">
        半角英数字で作るのがおすすめです（例：taro123）。
    </div>
</div>
```

**解説:**
- `form-text`: 入力欄の下に小さな説明文を表示
- ユーザーに入力のヒントを提供

---

## ボタン (Button)

Bootstrapは、様々な用途に応じたボタンスタイルを提供しています。

### 基本的なボタン

#### login.html の例

```html
<button type="submit" class="btn btn-primary w-100">
    ログインする
</button>
```

**解説:**
- `btn`: ボタンの基本スタイル（必須）
- `btn-primary`: 青色のボタン（主要アクション）
- `w-100`: 幅を100%に設定（親要素いっぱいに広がる）

### ボタンの色バリエーション

#### home.html の例

```html
<!-- 新規作成ボタン -->
<a href="{{ url_for('add_task') }}" class="btn btn-success">
    ＋ 新しいタスクを作る
</a>

<!-- 編集ボタン（アウトライン） -->
<a href="{{ url_for('edit_task', task_id=task_data.id) }}"
   class="btn btn-sm btn-outline-primary">編集</a>

<!-- 削除ボタン（アウトライン） -->
<button type="submit" class="btn btn-sm btn-outline-danger">削除</button>
```

**ボタンの色:**

| クラス | 色 | 用途 |
|--------|-----|------|
| `btn-primary` | 青（塗りつぶし） | 主要な操作 |
| `btn-success` | 緑（塗りつぶし） | 作成・追加 |
| `btn-danger` | 赤（塗りつぶし） | 削除 |
| `btn-secondary` | グレー（塗りつぶし） | キャンセル |
| `btn-outline-primary` | 青（枠線のみ） | 副次的な操作 |
| `btn-outline-danger` | 赤（枠線のみ） | 削除（目立ちすぎない） |

### ボタンのサイズ

```html
<!-- 小さいボタン -->
<a href="#" class="btn btn-sm btn-outline-primary">編集</a>

<!-- 通常サイズのボタン -->
<button type="submit" class="btn btn-primary">登録する</button>

<!-- 大きいボタン -->
<button type="submit" class="btn btn-lg btn-primary">送信</button>
```

**解説:**
- `btn-sm`: 小さいボタン（テーブル内のアクションに最適）
- デフォルト: 通常サイズ
- `btn-lg`: 大きいボタン

### グリッド配置ボタン

#### add_task.html の例

```html
<div class="d-grid gap-2">
    <button type="submit" class="btn btn-success">
        登録する
    </button>
    <a href="{{ url_for('home') }}" class="btn btn-secondary">一覧に戻る</a>
</div>
```

**解説:**
- `d-grid`: グリッドレイアウトを有効化
- `gap-2`: ボタン間の隙間を2段階分追加
- ボタンが縦に並び、それぞれが横幅いっぱいに広がる

### リンクをボタンにする

```html
<a href="{{ url_for('add_task') }}" class="btn btn-success">
    ＋ 新しいタスクを作る
</a>
```

**解説:**
- `<a>` タグに `btn` クラスを適用すると、リンクがボタンのように表示される
- ページ遷移用のアクションに使用

---

## バッジ (Badge)

バッジは、小さな色付きのラベルで、ステータスやカテゴリを表示するのに便利です。

### 基本的な使い方

#### home.html の例

```html
<td>
    {% if task_data.status.name == "NOT_STARTED" %}
    <span class="badge bg-secondary">未達成</span>

    {% elif task_data.status.name == "IN_PROGRESS" %}
    <span class="badge bg-primary">進行中</span>

    {% elif task_data.status.name == "COMPLETED" %}
    <span class="badge bg-success">実施済み</span>

    {% elif task_data.status.name == "PENDING" %}
    <span class="badge bg-warning">保留中</span>
    {% endif %}
</td>
```

**解説:**
- `badge`: バッジの基本スタイル
- `bg-*`: 背景色を指定（ボタンと同じ色が使える）
- 状態に応じて異なる色を使うことで、視覚的に分かりやすくなる

### バッジの色の使い分け

| ステータス | クラス | 色 | 意味 |
|-----------|--------|-----|------|
| 未達成 | `badge bg-secondary` | グレー | まだ始まっていない |
| 進行中 | `badge bg-primary` | 青 | 作業中 |
| 実施済み | `badge bg-success` | 緑 | 完了 |
| 保留中 | `badge bg-warning` | 黄色 | 一時停止 |

---

## テーブル (Table)

Bootstrapは、データを見やすく表示するためのテーブルスタイルを提供しています。

### 基本的なテーブル

#### home.html の例

```html
<table class="table table-striped">
    <thead>
        <tr>
            <th>ID</th>
            <th>タスク名</th>
            <th>状態</th>
            <th>作成日時</th>
            <th>操作</th>
        </tr>
    </thead>
    <tbody>
        {% for task_data in task_list %}
        <tr>
            <td>{{ task_data.id }}</td>
            <td>{{ task_data.task_name }}</td>
            <td><!-- バッジ --></td>
            <td>{{ task_data.created_at_jst }}</td>
            <td><!-- ボタン --></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

**解説:**

1. **基本スタイル** (`table`)
   - テーブルにBootstrapの基本スタイルを適用
   - 枠線、余白、フォントサイズが最適化される

2. **ストライプ** (`table-striped`)
   - 行ごとに背景色が交互に変わる
   - データが見やすくなる

### テーブルの種類

```html
<!-- ストライプ（縞模様） -->
<table class="table table-striped">...</table>

<!-- 枠線付き -->
<table class="table table-bordered">...</table>

<!-- ホバー効果 -->
<table class="table table-hover">...</table>

<!-- 組み合わせも可能 -->
<table class="table table-striped table-hover">...</table>
```

---

## ナビゲーションバー (Navbar)

ナビゲーションバーは、サイトの上部に配置されるメニューバーです。

### 基本的なナビゲーションバー

#### home.html の例

```html
<nav class="navbar navbar-dark bg-dark mb-4">
    <div class="container">
        <span class="navbar-brand">Todoアプリ</span>
        <a href="/logout" class="btn btn-outline-light btn-sm">ログアウト</a>
    </div>
</nav>
```

**解説:**

1. **ナビゲーションバー** (`navbar`)
   - ナビゲーションバーの基本スタイル

2. **ダークテーマ** (`navbar-dark`)
   - 文字色を白色に設定（暗い背景用）

3. **背景色** (`bg-dark`)
   - 背景を黒色に設定

4. **下部の余白** (`mb-4`)
   - ナビゲーションバーの下に余白を追加

5. **ブランド名** (`navbar-brand`)
   - サイト名やロゴを表示する領域
   - 大きめのフォントサイズになる

6. **コンテナ** (`container`)
   - 内容を中央揃えにして、左右に余白を作る

---

## ユーティリティクラス

Bootstrapには、レイアウトやスタイリングを簡単に調整できるユーティリティクラスがあります。

### 1. スペーシング（余白）

#### 記法
- `m`: margin（外側の余白）
- `p`: padding（内側の余白）
- `t`: top（上）
- `b`: bottom（下）
- `l`: left（左）
- `r`: right（右）
- `x`: 左右
- `y`: 上下
- `0-5`: サイズ（0が最小、5が最大）

#### 使用例

```html
<!-- 上の余白 -->
<div class="mt-5">...</div>  <!-- margin-top: 3rem -->

<!-- 下の余白 -->
<div class="mb-3">...</div>  <!-- margin-bottom: 1rem -->

<!-- 上下の余白 -->
<div class="my-4">...</div>  <!-- margin-top + bottom: 1.5rem -->

<!-- 内側の余白 -->
<div class="p-3">...</div>   <!-- padding: 1rem -->
```

#### このプロジェクトでの使用例

```html
<!-- login.html -->
<div class="container mt-5">  <!-- 上に大きめの余白 -->

<!-- add_task.html -->
<div class="mb-3">  <!-- フォーム要素の下に余白 -->

<!-- home.html -->
<nav class="navbar navbar-dark bg-dark mb-4">  <!-- ナビゲーションバーの下に余白 -->
```

### 2. 幅と高さ

```html
<!-- 幅100% -->
<button class="btn btn-primary w-100">ログインする</button>

<!-- 幅50% -->
<div class="w-50">...</div>

<!-- 高さ100% -->
<div class="h-100">...</div>
```

### 3. フレックスボックス

#### home.html の例

```html
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3>こんにちは、{{ current_user.login_id }}さん</h3>
    <a href="{{ url_for('add_task') }}" class="btn btn-success">
        ＋ 新しいタスクを作る
    </a>
</div>
```

**解説:**
- `d-flex`: フレックスボックスを有効化
- `justify-content-between`: 子要素を両端に配置（左右に分散）
- `align-items-center`: 子要素を垂直方向の中央に配置
- `mb-3`: 下に余白を追加

**結果:**
```
[こんにちは、ログイン中のユーザーさん]    [＋ 新しいタスクを作る]
     ← 左寄せ                                    右寄せ →
```

### 4. テキスト関連

```html
<!-- 文字色 -->
<div class="text-white">白色</div>
<div class="text-primary">青色</div>
<div class="text-muted">薄いグレー（補足テキスト）</div>

<!-- 文字揃え -->
<div class="text-center">中央揃え</div>
<div class="text-end">右揃え</div>
```

### 5. 表示・非表示

```html
<!-- インラインブロック表示 -->
<form style="display: inline;">...</form>

<!-- グリッド表示 -->
<div class="d-grid gap-2">...</div>
```

---

## 実践例：各ページの構造解説

### ログイン画面（login.html）

```html
<body class="bg-light">                          <!-- 背景を薄いグレーに -->
    <div class="container mt-5">                 <!-- コンテナ + 上余白 -->
        <div class="row justify-content-center"> <!-- 行 + 中央揃え -->
            <div class="col-md-6">               <!-- 50%幅の列 -->
                <div class="card">               <!-- カード -->
                    <div class="card-header bg-primary text-white">  <!-- 青いヘッダー -->
                        <h4>ログイン</h4>
                    </div>
                    <div class="card-body">      <!-- カード本体 -->
                        <form action="{{ url_for('login') }}" method="POST">
                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                            <div class="mb-3">   <!-- フォームグループ -->
                                <label class="form-label">ログインID</label>
                                <input class="form-control" ... />
                            </div>
                            <button class="btn btn-primary w-100">  <!-- 幅100%のボタン -->
                                ログインする
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
```

### タスク一覧画面（home.html）

```html
<nav class="navbar navbar-dark bg-dark mb-4">    <!-- 黒いナビゲーションバー -->
    <div class="container">
        <span class="navbar-brand">Todoアプリ</span>
        <form action="{{ url_for('logout') }}" method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
            <button type="submit" class="btn btn-outline-light btn-sm">ログアウト</button>
        </form>
    </div>
</nav>

<div class="container">
    <!-- タイトルと新規作成ボタンを左右に配置 -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>こんにちは、{{ current_user.login_id }}さん</h3>
        <a href="{{ url_for('add_task') }}" class="btn btn-success">
            ＋ 新しいタスクを作る
        </a>
    </div>

    <div class="card">                           <!-- カード -->
        <div class="card-body">
            <table class="table table-striped">  <!-- ストライプテーブル -->
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>タスク名</th>
                        <th>状態</th>
                        <th>作成日時</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {% for task_data in task_list %}
                    <tr>
                        <td>{{ task_data.id }}</td>
                        <td>{{ task_data.task_name }}</td>
                        <td>
                            <!-- バッジで状態を表示 -->
                            <span class="badge bg-success">実施済み</span>
                        </td>
                        <td>{{ task_data.created_at_jst }}</td>
                        <td>
                            <!-- 小さいアウトラインボタン -->
                            <a href="#" class="btn btn-sm btn-outline-primary">編集</a>
                            <button class="btn btn-sm btn-outline-danger">削除</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
```

### タスク編集画面（edit_task.html）

```html
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">                   <!-- 66.6%幅の列 -->
            <div class="card">
                <div class="card-header bg-primary text-white">  <!-- 青いヘッダー -->
                    <h4>タスクの編集</h4>
                </div>
                <div class="card-body">
                    <form action="{{ url_for('edit_task', task_id=task.id) }}" method="POST">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                        <div class="mb-3">
                            <label class="form-label">タスク名</label>
                            <input class="form-control"
                                   value="{{ task.task_name }}" />  <!-- 既存値を表示 -->
                        </div>

                        <div class="mb-3">
                            <label class="form-label">状態</label>
                            <select class="form-select">
                                <option value="NOT_STARTED"
                                    {% if task.status.name == "NOT_STARTED" %}selected{% endif %}>
                                    未達成
                                </option>
                                <!-- 他のオプション -->
                            </select>
                        </div>

                        <!-- ボタンを縦に並べる -->
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">更新する</button>
                            <a href="{{ url_for('home') }}" class="btn btn-secondary">一覧に戻る</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
```

---

## レスポンシブデザイン

Bootstrapは、画面サイズに応じて自動的にレイアウトが調整されます。

### ブレークポイント

| プレフィックス | 画面サイズ | デバイス |
|---------------|-----------|----------|
| `xs` | < 576px | スマートフォン（縦） |
| `sm` | ≥ 576px | スマートフォン（横） |
| `md` | ≥ 768px | タブレット |
| `lg` | ≥ 992px | 小型デスクトップ |
| `xl` | ≥ 1200px | デスクトップ |
| `xxl` | ≥ 1400px | 大型デスクトップ |

### 使用例

```html
<!-- タブレット以上で50%、それ以下で100% -->
<div class="col-md-6">...</div>

<!-- タブレット以上で66.6%、それ以下で100% -->
<div class="col-md-8">...</div>
```

**動作:**
- **スマートフォン**: `col-md-6` は無視され、100%幅になる
- **タブレット以上**: 50%幅になる

---

## まとめ

### このプロジェクトで使用されている主なBootstrapクラス

| カテゴリ | クラス | 用途 |
|---------|--------|------|
| **レイアウト** | `container`, `row`, `col-md-*` | 画面構成 |
| **カード** | `card`, `card-header`, `card-body` | コンテンツのボックス化 |
| **フォーム** | `form-label`, `form-control`, `form-select` | 入力フォーム |
| **ボタン** | `btn`, `btn-primary`, `btn-outline-*`, `btn-sm` | アクションボタン |
| **バッジ** | `badge`, `bg-*` | ステータス表示 |
| **テーブル** | `table`, `table-striped` | データ一覧 |
| **ナビゲーション** | `navbar`, `navbar-brand` | ヘッダーメニュー |
| **スペーシング** | `mt-*`, `mb-*`, `p-*` | 余白調整 |
| **フレックス** | `d-flex`, `justify-content-*` | 要素の配置 |
| **テキスト** | `text-white`, `text-muted` | 文字色 |

### Bootstrapを使うメリット

1. **開発速度の向上**: CSSを書かずにデザインが完成
2. **統一感のあるデザイン**: 全ページで一貫したUIを維持
3. **レスポンシブ対応**: モバイルでも自動的に最適表示
4. **メンテナンス性**: 標準的なクラス名で分かりやすい
5. **カスタマイズ可能**: 色やサイズを簡単に変更できる

### 学習のポイント

1. **基本構造を理解する**: Container → Row → Column
2. **クラスの命名規則を覚える**: `btn-primary`, `bg-success` など
3. **実際に使ってみる**: コードをコピーして試してみる
4. **公式ドキュメントを参照する**: https://getbootstrap.jp/

---

## 参考リンク

- [Bootstrap 公式サイト（英語）](https://getbootstrap.com/)
- [Bootstrap 日本語ドキュメント](https://getbootstrap.jp/)
- [Bootstrap CDN](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)

---

**作成日**: 2026年1月18日
**対象バージョン**: Bootstrap 5.3.0
**プロジェクト**: ToDoアプリケーション
