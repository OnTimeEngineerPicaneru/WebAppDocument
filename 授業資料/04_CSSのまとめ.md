# CSSのまとめ

> Webアプリ作成講座｜配布用教材 04

CSSは、HTMLで作った内容の色、文字、余白、配置などを整えるための言語です。この教材では、CSSの基本からFlexbox、Grid、レスポンシブデザインまでを学び、HTML教材で作った自己紹介ページをデザインします。

---

## 1. CSSとは

CSSは **Cascading Style Sheets** の略です。HTMLで表した内容と構造に対して、見た目や配置を指定します。ファイルの拡張子は `.css` です。

```text
HTML：見出し、段落、画像、リンクなどの意味と構造
CSS ：色、文字サイズ、余白、配置、画面幅への対応など
```

ブラウザーはCSSがなくても、見出しを大きくしたりリンクに下線を付けたりします。これはブラウザーが持つ標準のスタイルです。自分でCSSを書くと、そのスタイルを変更できます。

---

## 2. CSSの基本文法

```css
h1 {
  color: #1d4ed8;
  font-size: 2rem;
}
```

```text
h1       { color         : #1d4ed8; }
↑           ↑               ↑
セレクター  プロパティ      値

color: #1d4ed8; ＝ 宣言
{ ... }             ＝ 宣言ブロック
全体                 ＝ CSSルール
```

- **セレクター**：どのHTML要素へ適用するか
- **プロパティ**：何を変更するか
- **値**：どのように変更するか
- **宣言**：`プロパティ: 値;` の組み合わせ

宣言の最後にはセミコロン `;` を付けます。最後の宣言では省略できますが、追加や並べ替えでのミスを防ぐため、常に付けましょう。

### CSSのコメント

```css
/* ページ全体の文字を設定する */
body {
  color: #222222;
}
```

CSSのコメントは `/*` と `*/` で囲みます。`// コメント` は通常のCSSコメントではありません。

---

## 3. CSSをHTMLへ適用する

### 外部CSSを読み込む方法

実際の制作では、HTMLとCSSを別ファイルにする方法を基本とします。

```text
portfolio/
├─ index.html
└─ css/
   └─ style.css
```

`index.html`の`head`内で、CSSファイルを読み込みます。

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>わたしのポートフォリオ</title>
  <link rel="stylesheet" href="css/style.css">
</head>
```

- `rel="stylesheet"`：リンク先がスタイルシートだと示す
- `href="css/style.css"`：CSSファイルの場所を指定する

> 属性名は `href` です。`herf`ではありません。また、`←ここでCSSを適用`のような説明文をHTMLタグの途中へ書かないでください。

### HTML内のstyle要素

1ページだけで試す場合は、`head`内の`style`要素にもCSSを書けます。

```html
<style>
  h1 {
    color: navy;
  }
</style>
```

### style属性

```html
<p style="color: red;">赤い文字</p>
```

要素へ直接書く方法です。小さな実験には使えますが、再利用や管理が難しくなるため、通常の制作では外部CSSを使います。

### CSSが反映されないとき

1. HTMLとCSSを両方保存したか
2. ブラウザーを再読み込みしたか
3. `href`のファイルパスが正しいか
4. ファイル名の大文字と小文字が一致しているか
5. `{`、`}`、`:`、`;`が抜けていないか
6. セレクターがHTMLと一致しているか

---

## 4. セレクター

### 要素型セレクター

同じ種類の要素をすべて選びます。

```css
p {
  line-height: 1.8;
}
```

### classセレクター

HTMLの`class`属性へ付けた名前を、CSSでは先頭に `.` を付けて選びます。同じclassは複数の要素で使えます。

```html
<p class="message">新しい作品を公開しました。</p>
<p class="message">感想を募集中です。</p>
```

```css
.message {
  padding: 1rem;
  background-color: #eff6ff;
}
```

1つの要素へ複数のclassを付けることもできます。

```html
<a class="button button-primary" href="works.html">作品を見る</a>
```

### idセレクター

HTMLの`id`をCSSでは先頭に `#` を付けて選びます。idの値は1つのHTML文書内で重複させません。

```html
<section id="profile">...</section>
```

```css
#profile {
  scroll-margin-top: 2rem;
}
```

idはページ内リンクやJavaScriptから特定する用途にも使います。デザインの再利用には、基本的にclassが向いています。

### セレクターを組み合わせる

```css
/* navの中にあるa要素 */
nav a {
  color: #1d4ed8;
}

/* cardクラスを持つ要素の中のh2 */
.card h2 {
  margin-top: 0;
}

/* 複数のセレクターに同じ指定 */
h1,
h2,
h3 {
  line-height: 1.3;
}
```

セレクターを長く複雑にしすぎると、後から変更しにくくなります。

---

## 5. カスケード・詳細度・継承

CSSのCは **Cascading** のCです。同じ要素へ複数のルールが当たるとき、ブラウザーはどの宣言を使うか決めます。

### 後に書いた宣言

同じ強さのセレクターなら、後に書いた宣言が優先されます。

```css
p {
  color: blue;
}

p {
  color: green; /* こちらが使われる */
}
```

### 詳細度

より具体的なセレクターが優先されます。

```css
p {
  color: blue;
}

.notice {
  color: red; /* classの指定が優先される */
}
```

### 継承

`color`や`font-family`などは、親要素の値が子要素へ受け継がれることがあります。

```css
body {
  color: #222222;
  font-family: system-ui, sans-serif;
}
```

すべてのプロパティが継承されるわけではありません。たとえば`margin`や`border`は通常継承されません。

### !importantについて

`!important`は優先順位を強制的に上げますが、使いすぎると修正が難しくなります。まずセレクターや記述順を見直し、教材の基本制作では使わないようにしましょう。

---

## 6. 色と背景

### 色の指定方法

```css
.sample {
  color: #1f2937;
  background-color: rgb(239 246 255);
  border-color: hsl(217 91% 60%);
}
```

| 書き方 | 例 | 特徴 |
| --- | --- | --- |
| キーワード | `navy` | 名前で指定できるが、細かな調整には不向き |
| 16進数 | `#1d4ed8` | `#`と数字・A〜Fで表す |
| RGB | `rgb(29 78 216)` | 赤・緑・青の組み合わせ |
| HSL | `hsl(224 76% 48%)` | 色相・彩度・明度で表す |

### 透明度

```css
.overlay {
  background-color: rgb(0 0 0 / 60%);
}
```

`opacity`は要素全体と子要素も透明にします。背景だけを半透明にしたい場合は、色のアルファ値を使います。

### 配色の考え方

- **色相**：赤、黄、青などの色の種類
- **明度**：色の明るさ
- **彩度**：色の鮮やかさ
- **無彩色**：白、灰色、黒のように色味を持たない色

色の印象は文化、経験、組み合わせ、明るさによって変わります。「赤なら必ず食欲が増す」のように決めつけず、目的と読みやすさを優先します。

### コントラスト

文字と背景は十分に見分けられる組み合わせにします。一般的な大きさの文字では **4.5:1以上**、大きな文字では **3:1以上** のコントラスト比が目安です。

```css
/* 読みにくい例 */
.low-contrast {
  color: #dddddd;
  background-color: #ffffff;
}

/* 読みやすい例 */
.readable {
  color: #1f2937;
  background-color: #ffffff;
}
```

色だけで状態を伝えず、文字や記号も使います。

```html
<p class="error"><strong>エラー：</strong>名前を入力してください。</p>
```

---

## 7. 文字を整える

```css
body {
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 1rem;
  line-height: 1.7;
  color: #1f2937;
}

h1 {
  font-size: 2rem;
  line-height: 1.3;
  letter-spacing: 0.03em;
}
```

| プロパティ | 役割 |
| --- | --- |
| `font-family` | フォントの候補を指定する |
| `font-size` | 文字サイズ |
| `font-weight` | 文字の太さ |
| `line-height` | 行の高さ |
| `letter-spacing` | 文字間隔 |
| `text-align` | 行内方向のそろえ方 |
| `text-decoration` | 下線などの装飾 |

`font-family`は、先頭の候補が使えなければ次の候補へ進みます。空白を含むフォント名は引用符で囲み、最後に`serif`や`sans-serif`などの一般ファミリーを指定します。

### Webフォント

Google FontsなどのWebフォントも利用できます。ただし、外部通信や読み込み時間、利用規約、文字セット、個人情報への影響を確認します。Webフォントを読み込めない場合に備えて、代替フォントも指定しましょう。

---

## 8. CSSの単位

| 単位 | 意味 | おもな用途 |
| --- | --- | --- |
| `px` | CSSピクセル | 細い罫線など |
| `%` | 親要素などに対する割合 | 幅など |
| `rem` | ルート要素の文字サイズに対する倍率 | 文字、余白 |
| `em` | その要素の文字サイズなどに対する倍率 | 部品内の余白など |
| `vw` | 表示領域の幅の1% | 画面幅に応じる大きさ |
| `vh` | 表示領域の高さの1% | 画面高に応じる大きさ |
| `fr` | Grid内の利用可能な空間の割合 | Gridの列や行 |

すべてを固定の`px`で決めると、画面幅や文字サイズの変更に対応しにくいことがあります。目的に応じて相対単位も使います。

```css
.container {
  width: min(100% - 2rem, 60rem);
  margin-inline: auto;
}
```

この例は、左右に余白を残しながら、内容を最大`60rem`の幅にします。

---

## 9. ボックスモデル

CSSでは多くの要素を四角い箱として考えます。

```text
┌──────────── margin ────────────┐
│  ┌──────── border ──────────┐  │
│  │  ┌───── padding ──────┐  │  │
│  │  │      content       │  │  │
│  │  └────────────────────┘  │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
```

- **content**：文章や画像が入る領域
- **padding**：内容と枠線の間の内側余白
- **border**：枠線
- **margin**：ほかの要素との間の外側余白

```css
.card {
  margin: 1rem 0;
  border: 1px solid #d1d5db;
  padding: 1.5rem;
  background-color: white;
  border-radius: 0.75rem;
}
```

### box-sizing

標準の計算では、指定した`width`にpaddingとborderが加算されます。`border-box`を使うと、それらを指定幅の内側に含められます。

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

### marginとpaddingの一括指定

```css
.box-a {
  margin: 1rem;                 /* 上下左右 */
}

.box-b {
  margin: 1rem 2rem;            /* 上下、左右 */
}

.box-c {
  margin: 1rem 2rem 3rem;       /* 上、左右、下 */
}

.box-d {
  margin: 1rem 2rem 3rem 4rem;  /* 上、右、下、左 */
}
```

時計回りに「上・右・下・左」と覚えます。

---

## 10. 画像や表、フォームを整える

### 画像

```css
img {
  display: block;
  max-width: 100%;
  height: auto;
}
```

画像が親要素より大きくならず、縦横比を保って縮小されます。

### 表

```css
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #cbd5e1;
  padding: 0.75rem;
  text-align: left;
}

thead {
  background-color: #eff6ff;
}

tbody tr:nth-child(even) {
  background-color: #f8fafc;
}
```

HTMLの`border`属性ではなくCSSで罫線を指定します。

### フォーム

```css
input,
textarea,
select,
button {
  font: inherit;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #94a3b8;
  border-radius: 0.375rem;
}

button {
  padding: 0.75rem 1rem;
  border: 0;
  border-radius: 0.375rem;
  color: white;
  background-color: #1d4ed8;
  cursor: pointer;
}
```

ラジオボタンとチェックボックスに`width: 100%`を適用すると不自然になります。必要な入力型だけを選ぶ方法もあります。

```css
input:not([type="radio"]):not([type="checkbox"]),
textarea,
select {
  width: 100%;
}
```

---

## 11. 疑似クラスと状態

疑似クラスは、要素の状態などを選びます。

```css
a {
  color: #1d4ed8;
}

a:visited {
  color: #6d28d9;
}

a:hover {
  color: #1e40af;
}

a:focus-visible,
button:focus-visible,
input:focus-visible {
  outline: 3px solid #f59e0b;
  outline-offset: 3px;
}
```

- `:hover`：マウスポインターなどが要素の上にある状態
- `:focus-visible`：キーボード操作などでフォーカスを見せる必要がある状態
- `:checked`：チェックボックスなどが選択された状態
- `:disabled`：操作できない状態
- `:nth-child()`：兄弟要素の位置で選ぶ

`hover`だけで情報を伝えると、タッチ操作やキーボード操作では利用できません。`focus-visible`なども用意します。ブラウザー標準のフォーカス枠を消すだけの`outline: none`は避けます。

---

## 12. Flexbox：一方向のレイアウト

Flexboxは、項目を行または列という **1つの方向** に並べ、そろえるのが得意です。親要素をflexコンテナー、直接の子要素をflexアイテムと呼びます。

```html
<ul class="menu">
  <li><a href="#profile">自己紹介</a></li>
  <li><a href="#works">作品</a></li>
  <li><a href="#contact">連絡先</a></li>
</ul>
```

```css
.menu {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin: 0;
  padding: 0;
  list-style: none;
}
```

### 主軸と交差軸

`flex-direction: row`では主軸が横方向、交差軸が縦方向です。`column`にすると方向も入れ替わります。

```css
.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
```

| プロパティ | 役割 |
| --- | --- |
| `flex-direction` | 主軸の方向を決める |
| `justify-content` | 主軸方向の配置を決める |
| `align-items` | 交差軸方向で、各アイテムの配置を決める |
| `flex-wrap` | 入りきらない項目を折り返すか決める |
| `gap` | 項目間のすき間を決める |
| `align-content` | 複数行全体の交差軸方向の配置を決める |

`justify-content`の代表的な値：

- `flex-start`：主軸の開始側
- `flex-end`：主軸の終了側
- `center`：中央
- `space-between`：両端に置き、項目間を均等にする
- `space-around`：各項目の周りへ均等な空間を割り当てる
- `space-evenly`：両端と項目間の空間を同じにする

左右や上下という言葉だけで覚えると、`flex-direction`変更時に混乱します。主軸と交差軸で考えましょう。

---

## 13. Grid：行と列のレイアウト

CSS Gridは、行と列という **2つの方向** を使うレイアウトが得意です。

```html
<div class="work-grid">
  <article class="card">作品1</article>
  <article class="card">作品2</article>
  <article class="card">作品3</article>
  <article class="card">作品4</article>
</div>
```

```css
.work-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
```

- `grid-template-columns`：列の数と幅
- `1fr`：利用できる空間を分けた1単位
- `repeat(2, 1fr)`：同じ幅の列を2つ作る
- `gap`：行と列のすき間

画面幅に応じて、入る数だけ列を作ることもできます。

```css
.work-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: 1rem;
}
```

### FlexboxとGridの選び方

| 目的 | 向いている方法 |
| --- | --- |
| メニューを横一列に並べる | Flexbox |
| ボタンと文字を1方向にそろえる | Flexbox |
| カードを行と列に並べる | Grid |
| ページの複数領域を行と列で設計する | Grid |

どちらか一方しか使えないわけではありません。Gridのカード内でFlexboxを使うなど、組み合わせられます。

---

## 14. レスポンシブデザイン

レスポンシブデザインは、さまざまな画面幅や端末で内容を利用しやすくする考え方です。特定の機種だけに合わせず、内容が窮屈になった地点でレイアウトを変更します。

### モバイルファースト

まず狭い画面向けの基本スタイルを書き、広い画面で必要な変更をメディアクエリーに追加します。

```css
.profile {
  display: grid;
  gap: 1rem;
}

@media (min-width: 48rem) {
  .profile {
    grid-template-columns: 1fr 2fr;
    align-items: center;
  }
}
```

`48rem`は機種名ではなく、このページの内容が2列でも読みやすくなる地点として決めます。

### 横にはみ出させない

```css
img,
video {
  max-width: 100%;
  height: auto;
}

body {
  overflow-wrap: break-word;
}
```

内容を隠すためだけに`overflow-x: hidden`を指定すると、本当の表示崩れに気づけない場合があります。まず、はみ出す原因を直します。

---

## 15. CSSカスタムプロパティ

同じ色や余白を何度も使う場合は、カスタムプロパティへ名前を付けられます。

```css
:root {
  --color-primary: #1d4ed8;
  --color-text: #1f2937;
  --color-surface: #ffffff;
  --space-md: 1rem;
  --radius-md: 0.5rem;
}

.card {
  padding: var(--space-md);
  color: var(--color-text);
  background-color: var(--color-surface);
  border-radius: var(--radius-md);
}

.button {
  background-color: var(--color-primary);
}
```

色の値だけでなく役割がわかる名前にすると、サイト全体を変更しやすくなります。

---

## 16. 総合実習：自己紹介ページをデザインする

HTML教材で作った`index.html`と同じフォルダーに`css/style.css`を作り、次のCSSから始めましょう。

```css
/* 基本設定 */
*,
*::before,
*::after {
  box-sizing: border-box;
}

:root {
  --color-primary: #1d4ed8;
  --color-primary-dark: #1e3a8a;
  --color-text: #1f2937;
  --color-muted: #475569;
  --color-surface: #ffffff;
  --color-background: #f1f5f9;
  --color-border: #cbd5e1;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  color: var(--color-text);
  background-color: var(--color-background);
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  line-height: 1.7;
}

img {
  display: block;
  max-width: 100%;
  height: auto;
}

a {
  color: var(--color-primary);
}

a:hover {
  color: var(--color-primary-dark);
}

a:focus-visible,
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
  outline: 3px solid #f59e0b;
  outline-offset: 3px;
}

header,
nav,
main,
footer {
  width: min(100% - 2rem, 64rem);
  margin-inline: auto;
}

header,
footer {
  padding-block: 2rem;
  text-align: center;
}

h1,
h2,
h3 {
  line-height: 1.3;
}

h1 {
  color: var(--color-primary-dark);
}

nav ul {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

nav a {
  display: block;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 700;
  text-decoration: none;
}

nav a:hover {
  background-color: #dbeafe;
}

main {
  display: grid;
  gap: 1.5rem;
  padding-block: 2rem;
}

section {
  padding: 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: 0.75rem;
  background-color: var(--color-surface);
  box-shadow: 0 0.25rem 0.75rem rgb(15 23 42 / 8%);
}

section h2 {
  margin-top: 0;
  padding-bottom: 0.5rem;
  border-bottom: 0.2rem solid var(--color-primary);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  text-align: left;
}

input:not([type="radio"]):not([type="checkbox"]),
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #94a3b8;
  border-radius: 0.375rem;
  font: inherit;
}

button {
  padding: 0.75rem 1rem;
  border: 0;
  border-radius: 0.375rem;
  color: white;
  background-color: var(--color-primary);
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

@media (min-width: 48rem) {
  main {
    grid-template-columns: repeat(2, 1fr);
  }

  main > section:last-child {
    grid-column: 1 / -1;
  }
}
```

### 必須ミッション

- [ ] 外部CSSを正しい`href`で読み込む
- [ ] セレクター、プロパティ、値を使って3か所以上変更する
- [ ] 文字色と背景色を読みやすい組み合わせにする
- [ ] `margin`と`padding`を使い分ける
- [ ] `box-sizing: border-box`を設定する
- [ ] classを1つ以上追加して再利用する
- [ ] FlexboxまたはGridを使う
- [ ] `:hover`と`:focus-visible`の両方を用意する
- [ ] 画像が画面からはみ出さないようにする
- [ ] 狭い画面と広い画面で確認する

### 発展ミッション

- [ ] CSSカスタムプロパティで配色を管理する
- [ ] Gridで作品カードを自動的に折り返す
- [ ] メディアクエリーでレイアウトを変更する
- [ ] 表やフォームを読みやすく整える
- [ ] 開発者ツールでボックスモデルを確認する

---

## 17. テストとデバッグ

### 画面幅を変える

ブラウザーの幅を少しずつ狭くし、次を確認します。

- 横スクロールが発生しないか
- 文字やボタンが重ならないか
- メニューが自然に折り返すか
- 画像や表が画面からはみ出さないか
- 文章の1行が長すぎないか

### キーボードで操作する

`Tab`キーでリンク、ボタン、フォームへ移動し、現在位置が見えるか確認します。

### ブラウザーの開発者ツール

要素を調べる機能を使うと、次を確認できます。

- どのCSSルールが適用されているか
- 上書きされて使われていない宣言はどれか
- margin、border、padding、contentの大きさ
- 画面幅を変えたときの表示

開発者ツールで変更した内容は、通常は元のCSSファイルへ自動保存されません。うまくいった値をCSSへ書き戻します。

---

## 18. よくある間違い

### hrefの綴りやパスが違う

```html
<!-- 間違い -->
<link rel="stylesheet" herf="style.css">

<!-- 正しい -->
<link rel="stylesheet" href="css/style.css">
```

### HTMLのclassとCSSが一致しない

```html
<section class="works">...</section>
```

```css
.work { /* worksではないため適用されない */
  background: white;
}
```

### classの先頭の点を忘れる

```css
/* class="card"を選ぶ */
.card {
  padding: 1rem;
}
```

### 単位を忘れる

```css
/* 間違い */
padding: 20;

/* 正しい */
padding: 20px;
```

`0`には単位がなくてもかまいません。

### 全角記号や全角空白が入る

コードでは半角の `{ } : ;` を使います。説明用の矢印などをコード内へ入れないでください。

### 波かっこの対応が取れていない

```css
.card {
  color: #222222;
  background-color: white;
}
```

字下げをそろえると、閉じ波かっこの不足に気づきやすくなります。

---

## 19. 確認問題

1. HTMLとCSSは、それぞれ何を担当しますか。
2. 外部CSSを読み込む`link`要素で、ファイルの場所を指定する属性は何ですか。
3. セレクター、プロパティ、値を説明してください。
4. classとidの違いは何ですか。
5. ボックスモデルを構成する4つの領域を挙げてください。
6. FlexboxとGridは、それぞれどのような配置が得意ですか。
7. `:hover`だけでなく`:focus-visible`も設定する理由は何ですか。
8. メディアクエリーは何のために使いますか。

<details>
<summary>解答例</summary>

1. HTMLは内容と構造、CSSは見た目と配置を担当する。
2. `href`属性。
3. セレクターは対象、プロパティは変更する項目、値は変更内容。
4. classは同じ文書内で複数の要素に再利用でき、idは文書内で重複しない識別名。
5. content、padding、border、margin。
6. Flexboxは行か列という一方向、Gridは行と列の二方向の配置が得意。
7. マウスを使わずキーボードで操作する人にも、現在位置を見えるようにするため。
8. 画面幅などの条件に応じて適用するCSSを変更するため。

</details>

---

## まとめ

- CSSはHTMLの見た目と配置を整える言語
- 外部CSSは`link`要素の`href`属性で読み込む
- CSSはセレクターと宣言ブロックからなる
- classは再利用するデザイン、idは重複しない識別に向く
- カスケード、詳細度、継承によって使われる宣言が決まる
- margin、border、padding、contentがボックスを作る
- Flexboxは一方向、Gridは行と列の配置が得意
- レスポンシブ対応では、内容に合わせて柔軟にレイアウトを変える
- 色、フォーカス、画面幅に配慮し、さまざまな利用者が使えるデザインにする

## 参考資料

- [元教材：CSSまとめ（Notion）](https://app.notion.com/p/323b4d037411804c95ecd5d6e53a159f)
- [MDN Web Docs「What is CSS?」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/What_is_CSS)
- [MDN Web Docs「Basic CSS selectors」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors)
- [MDN Web Docs「The box model」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [MDN Web Docs「Flexbox」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox)
- [MDN Web Docs「CSS grid layout」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids)
- [MDN Web Docs「Responsive web design」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design)
- [W3C WAI「Understanding Success Criterion 1.4.3: Contrast (Minimum)」](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)

※外部サイトやサービスの内容、URL、利用条件は変更されることがあります。
