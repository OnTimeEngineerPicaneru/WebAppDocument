# HTMLのまとめ

> Webアプリ作成講座｜配布用教材 03

HTMLは、Webページの内容と構造を表すための言語です。この教材では、基本の書き方から、画像、リンク、表、フォームまでを順番に学び、最後に自己紹介ページを完成させます。

---

## 1. HTMLとは

HTMLは **HyperText Markup Language** の略です。Webページにある文章や画像などへ「これは見出し」「これは段落」「これはリンク」という意味と構造を与える、マークアップ言語です。

```html
<h1>わたしの好きなもの</h1>
<p>このページでは、好きな本を紹介します。</p>
```

`h1`は最も上位の見出し、`p`は段落を表します。ブラウザーはHTMLを読み取り、それぞれの意味に応じてページを組み立てます。

> HTMLの要素が、そのままボタンやメニューバーの見た目になるとは限りません。HTMLはおもに意味と構造、CSSはおもに見た目、JavaScriptはおもに動きや処理を担当します。

---

## 2. 要素・タグ・属性

次のコードを分解してみましょう。

```html
<a href="https://example.com">サンプルサイトを見る</a>
```

```text
開始タグ                         内容                 終了タグ
<a href="https://example.com"> サンプルサイトを見る </a>
   └──────── 属性 ────────┘

開始タグ + 内容 + 終了タグ = 要素
```

- **要素**：ページを構成する部品全体
- **タグ**：要素の始まりや終わりを示す記号
- **属性**：要素へ追加情報を与える設定
- **属性値**：属性に設定する値。通常は引用符 `"` で囲む

### 終了タグがない要素

`img`や`meta`など、終了タグを持たない要素もあります。この教材では次のように書きます。

```html
<img src="cat.jpg" alt="眠っている白い猫">
```

`<img ... />`のように最後へ `/` を付けてもHTMLでは動作しますが、必須ではありません。書き方を統一しましょう。

### 正しい入れ子

要素の中に別の要素を置くことを「入れ子」といいます。後から開いた要素を先に閉じます。

```html
<!-- 正しい -->
<p>今日は<strong>大切なお知らせ</strong>があります。</p>

<!-- 間違い -->
<p>今日は<strong>大切なお知らせ</p></strong>
```

---

## 3. HTMLファイルを作る

### ファイルを準備する

1. 作業用フォルダーを作る
2. コードエディターで新しいファイルを作る
3. `index.html` という名前で保存する
4. 次のコードを入力する
5. 保存してブラウザーで開く

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="HTMLを学ぶための自己紹介ページです。">
    <title>わたしの自己紹介</title>
  </head>
  <body>
    <h1>わたしの自己紹介</h1>
    <p>はじめまして。HTMLを勉強しています。</p>
  </body>
</html>
```

### 骨組みの意味

| コード | 役割 |
| --- | --- |
| `<!doctype html>` | 現在の標準的なHTMLとして表示するようブラウザーへ伝える |
| `<html lang="ja">` | 文書全体を囲み、主な言語が日本語だと示す |
| `<head>` | ページについての設定や情報をまとめる |
| `<meta charset="UTF-8">` | 文字コードをUTF-8にする |
| `<meta name="viewport" ...>` | 端末の画面幅に合わせて表示するための設定 |
| `<meta name="description" ...>` | ページ内容の短い説明を設定する |
| `<title>` | ブラウザーのタブやブックマークなどに使われる題名 |
| `<body>` | 利用者に表示する内容をまとめる |

`doctype`は、古い表示方法へ切り替わるのを防ぐために必要です。「HTMLのバージョンを細かく指定する場所」と覚える必要はありません。

> `meta name="keywords"` は、現在のおもな検索エンジン対策として役立つとはいえないため、この教材の基本形には入れません。

---

## 4. ファイル名とフォルダー

Web制作では、ファイルの場所を間違えないことが大切です。

```text
portfolio/
├─ index.html
└─ images/
   └─ camera.jpg
```

この場合、`index.html`から画像を指定するときは次のように書きます。

```html
<img src="images/camera.jpg" alt="机の上に置かれたカメラ">
```

### ファイル名のルール

- 半角英数字を基本にする：`profile.html`
- 単語の区切りにはハイフンを使う：`club-activity.html`
- HTMLには `.html` を付ける
- 大文字と小文字を区別する：`Photo.jpg` と `photo.jpg` は別名として扱われることがある
- 空白、全角文字、記号はURLで特別な表現へ変換される場合があるため、初学者は避ける
- 内容がわかる名前を付ける：`page1.html` より `contact.html`

全角文字が「サーバーに存在しない」わけではありません。しかし、入力やURLの扱いで間違いが起きやすいため、この講座では半角英数字とハイフンに統一します。

---

## 5. 文章を構造化する

### 見出し

```html
<h1>わたしのポートフォリオ</h1>

<h2>自己紹介</h2>
<p>好きなことや得意なことを紹介します。</p>

<h2>作品</h2>
<h3>クイズアプリ</h3>
<p>学校の授業で制作しました。</p>
```

`h1`から`h6`の数字は、単なる文字サイズではなく見出しの階層を表します。`h1`の次を見た目だけの理由で`h4`に飛ばすのは避け、文書の構造に合わせて選びます。

### 段落と改行

```html
<p>これは1つ目の段落です。</p>
<p>これは2つ目の段落です。</p>
```

新しい段落には`p`を使います。住所や詩のように、同じまとまりの中で改行自体に意味がある場合は`br`を使えます。

```html
<p>
  〒000-0000<br>
  東京都サンプル区1-2-3
</p>
```

余白を作るために`<br><br>`を繰り返すのは避けます。見た目の間隔はCSSで指定します。

### 大切さと強調

```html
<p>申し込みは<strong>金曜日まで</strong>です。</p>
<p>わたしは<em>とても</em>楽しみにしています。</p>
```

- `strong`：内容の重要性や重大さを表す
- `em`：文章の中で強調して読む部分を表す

太字や斜体にしたいだけなら、見た目はCSSで設定します。

### リスト

順番に意味がない箇条書きには`ul`を使います。

```html
<ul>
  <li>写真撮影</li>
  <li>読書</li>
  <li>プログラミング</li>
</ul>
```

手順や順位には`ol`を使います。

```html
<ol>
  <li>ファイルを保存する</li>
  <li>ブラウザーで開く</li>
  <li>表示を確認する</li>
</ol>
```

用語と説明の組み合わせには`dl`、`dt`、`dd`を使えます。

```html
<dl>
  <dt>HTML</dt>
  <dd>Webページの内容と構造を表す言語</dd>
  <dt>CSS</dt>
  <dd>Webページの見た目を整える言語</dd>
</dl>
```

---

## 6. リンクを作る

### 別のサイトへのリンク

```html
<a href="https://developer.mozilla.org/ja/">MDN Web Docsで調べる</a>
```

### 同じサイトの別ページへのリンク

```html
<a href="works.html">作品一覧を見る</a>
```

### 同じページ内の場所へのリンク

移動先へ重複しない`id`を付け、その値の前に`#`を付けて指定します。

```html
<a href="#works">作品へ移動</a>

<section id="works">
  <h2>作品</h2>
  <p>制作した作品を紹介します。</p>
</section>
```

ページ先頭へ戻るリンクを作るなら、実際に移動先を用意します。

```html
<body id="top">
  <!-- ページの内容 -->
  <a href="#top">ページの先頭へ戻る</a>
</body>
```

### 新しいタブで開く場合

```html
<a href="https://example.com" target="_blank" rel="noopener">
  サンプルサイト（新しいタブで開く）
</a>
```

新しいタブで開くことが利用者に伝わる文章にします。何でも新しいタブにせず、本当に必要な場合だけ使いましょう。

### よいリンクの文章

```html
<!-- わかりにくい -->
<a href="schedule.html">こちら</a>

<!-- わかりやすい -->
<a href="schedule.html">活動スケジュールを見る</a>
```

リンクだけを読み上げても、移動先がわかる文章にします。

---

## 7. 画像を表示する

```html
<img
  src="images/camera.jpg"
  alt="夕焼けを撮影している黒いカメラ"
  width="400"
  height="300"
>
```

- `src`：画像ファイルの場所
- `alt`：画像を見られないときに代わりとなる文章
- `width`、`height`：画像の表示寸法。縦横比に合う値を指定する

### altの考え方

同じ画像でも、ページ内での役割によって`alt`は変わります。

```html
<!-- 内容を伝える写真 -->
<img src="club.jpg" alt="体育館でバスケットボールを練習する部員">

<!-- 内容を持たない飾り -->
<img src="decoration.svg" alt="">
```

「画像」「写真」のような言葉だけでなく、その画像から伝えたい内容を書きます。画像のすぐ近くに同じ説明がある場合は、重複して読まれないよう空の`alt`が適切なこともあります。

### 画像と説明をまとめる

```html
<figure>
  <img src="images/work.jpg" alt="青色を基調にした天気予報アプリの画面">
  <figcaption>授業で制作した天気予報アプリ</figcaption>
</figure>
```

`figure`は画像などのまとまり、`figcaption`はその説明やキャプションを表します。

### 外部のサンプル画像

[Lorem Picsum](https://picsum.photos/)のように、URLからサンプル画像を表示できるサービスもあります。ただし、次の点に注意してください。

- サービスが停止すると画像を表示できない
- 表示内容が毎回変わる場合がある
- 利用条件や年齢制限を確認する
- 完成作品では、内容に合う許可済みの画像を自分のフォルダーに保存して使う

---

## 8. ページの大きな構造

意味に合った要素を使う書き方を **セマンティックHTML** といいます。

```html
<body id="top">
  <header>
    <h1>わたしのポートフォリオ</h1>
    <p>制作した作品を紹介します。</p>
  </header>

  <nav aria-label="メインメニュー">
    <ul>
      <li><a href="#profile">自己紹介</a></li>
      <li><a href="#works">作品</a></li>
    </ul>
  </nav>

  <main>
    <section id="profile">
      <h2>自己紹介</h2>
      <p>プログラミングを勉強している中学生です。</p>
    </section>

    <section id="works">
      <h2>作品</h2>
      <article>
        <h3>クイズアプリ</h3>
        <p>三択問題に挑戦できるアプリです。</p>
      </article>
    </section>
  </main>

  <footer>
    <p><small>&copy; 2026 Sample Student</small></p>
    <p><a href="#top">ページの先頭へ戻る</a></p>
  </footer>
</body>
```

| 要素 | おもな意味 |
| --- | --- |
| `header` | ページや区画の導入部分 |
| `nav` | おもな移動用リンクのまとまり |
| `main` | ページ固有の中心的な内容。通常、文書内に1つ |
| `section` | 1つのテーマを持つ内容のまとまり。通常は見出しを付ける |
| `article` | 単独でも意味が通る記事や作品など |
| `footer` | ページや区画についての補足、著作権、連絡先など |

`header`と`footer`は、必ず画面の最上部・最下部に固定されるという意味ではありません。どのように配置するかはCSSで決めます。

---

## 9. 表を作る

表は、時間割や成績一覧のような、行と列の関係を持つデータに使います。ページ全体のレイアウトには使いません。

```html
<table>
  <caption>制作した作品</caption>
  <thead>
    <tr>
      <th scope="col">作品名</th>
      <th scope="col">内容</th>
      <th scope="col">使用技術</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">クイズアプリ</th>
      <td>三択クイズに挑戦できる</td>
      <td>HTML、CSS、JavaScript</td>
    </tr>
    <tr>
      <th scope="row">自己紹介ページ</th>
      <td>趣味や作品を紹介する</td>
      <td>HTML、CSS</td>
    </tr>
  </tbody>
</table>
```

| 要素 | 意味 |
| --- | --- |
| `table` | 表全体 |
| `caption` | 表の題名や説明 |
| `thead` | 見出し行のまとまり |
| `tbody` | おもなデータ行のまとまり |
| `tr` | 1つの行 |
| `th` | 行や列の見出しセル |
| `td` | データのセル |

`border="1"`のような見た目の指定はHTMLへ書かず、罫線や色はCSSで設定します。

---

## 10. フォームを作る

フォームは、検索、ログイン、アンケートなど、利用者が情報を入力する場面で使います。

```html
<form action="/contact" method="post">
  <p>
    <label for="name">名前</label>
    <input type="text" id="name" name="user_name" required>
  </p>

  <p>
    <label for="email">メールアドレス</label>
    <input type="email" id="email" name="user_email" required>
  </p>

  <fieldset>
    <legend>お問い合わせの種類</legend>

    <label>
      <input type="radio" name="contact_type" value="question" required>
      質問
    </label>

    <label>
      <input type="radio" name="contact_type" value="impression">
      感想
    </label>
  </fieldset>

  <p>
    <label for="message">内容</label><br>
    <textarea id="message" name="message" rows="5" required></textarea>
  </p>

  <p>
    <label for="source">このページを知ったきっかけ</label>
    <select id="source" name="source">
      <option value="">選択してください</option>
      <option value="school">学校</option>
      <option value="friend">友達</option>
      <option value="search">検索</option>
    </select>
  </p>

  <button type="submit">入力内容を送信</button>
</form>
```

### 属性の意味

| 属性 | 意味 |
| --- | --- |
| `action` | 入力データの送信先 |
| `method` | 送信方法。代表例は`get`と`post` |
| `type` | 入力欄やボタンの種類 |
| `id` | ページ内で要素を識別する名前 |
| `for` | `label`と入力欄を結び付ける。入力欄の`id`と同じ値にする |
| `name` | 送信するデータの項目名 |
| `value` | 選択肢などで送信する値 |
| `required` | 入力や選択を必須にする |

### labelが大切な理由

`label`を入力欄と正しく結び付けると、次の利点があります。

- 何を入力する欄か読み上げソフトに伝わる
- ラベルの文字をクリックしても入力欄を選べる
- 利用者が入力内容を間違えにくくなる

ラジオボタンのような関連する選択肢は、`fieldset`と`legend`で1つのグループにします。

### フォームはHTMLだけでは送信を完了できない

HTMLで入力欄を表示できても、入力内容を保存したりメールで届けたりするには、送信先のサーバー側プログラムやフォームサービスが必要です。`action="#"`は実際の送信先ではありません。

授業で送信処理をまだ作っていない場合は、次のように通常のボタンとして見た目と操作だけを確認できます。

```html
<button type="button">送信処理はまだありません</button>
```

個人情報を扱うフォームは、保存場所、利用目的、閲覧できる人、削除方法を決めてから公開します。

---

## 11. 特殊な文字とコメント

HTMLで特別な意味を持つ文字をそのまま表示したい場合は、文字参照を使います。

| 表示したい文字 | HTMLでの書き方 |
| --- | --- |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `©` | `&copy;` |

ブラウザーに表示しないメモは、コメントとして書けます。

```html
<!-- ここから作品紹介の区画 -->
<section>
  <h2>作品</h2>
</section>
```

コメントもファイルを見れば読めます。パスワードや個人情報など、秘密の内容は書かないでください。

---

## 12. セマンティックHTMLとアクセシビリティ

HTML要素を見た目ではなく意味に合わせて選ぶと、次の人や仕組みに内容が伝わりやすくなります。

- 画面を見て読む人
- 読み上げソフトを使う人
- キーボードで操作する人
- 検索エンジン
- 後からコードを直す自分やほかの制作者

### よくある改善例

```html
<!-- 見た目だけでボタンのようにした要素 -->
<div>送信</div>

<!-- 意味と機能を持つボタン -->
<button type="button">送信</button>
```

```html
<!-- 見た目を大きくする目的で見出しを使う -->
<h1>注意書き</h1>

<!-- 文書構造に合う段落として書き、見た目はCSSで調整する -->
<p><strong>注意：</strong>送信前に内容を確認してください。</p>
```

正しい要素を使うと、ブラウザーが持つキーボード操作や読み上げ支援を利用しやすくなります。

---

## 13. 総合制作：自己紹介ページ

ここまでに学んだ内容を使い、自己紹介または架空の人物・キャラクターの紹介ページを作りましょう。自分の個人情報を公開する必要はありません。

### 必須ミッション

- [ ] HTMLの基本構造がある
- [ ] `lang="ja"`を指定している
- [ ] 内容がわかる`title`と`description`がある
- [ ] `header`、`nav`、`main`、`footer`を使っている
- [ ] `h1`を1つ、`h2`を2つ以上使っている
- [ ] 段落とリストを使っている
- [ ] ページ内リンクを使っている
- [ ] 画像と内容に合う`alt`がある
- [ ] `figure`と`figcaption`を1組使っている
- [ ] 表またはフォームのどちらかを使っている
- [ ] 開始タグと終了タグの入れ子が正しい

### 発展ミッション

- [ ] 定義リストで用語と説明をまとめる
- [ ] 表に`caption`と見出しセルを付ける
- [ ] フォームの全入力欄に`label`を付ける
- [ ] ラジオボタンを`fieldset`でまとめる
- [ ] 別ページを作り、相対URLでリンクする

### 完成後のテスト

1. ファイルを保存して再読み込みする
2. ブラウザーのタブに正しい題名が出るか確認する
3. すべてのリンクを押す
4. 画像のファイル名を一時的に変え、`alt`の内容を確認する
5. `Tab`キーでリンクやフォームへ移動できるか確認する
6. HTMLの字下げと入れ子を見直す
7. 友達にページの構造と内容を確認してもらう

---

## 14. よくある間違い

### 保存後に再読み込みしていない

コードを直したらファイルを保存し、ブラウザーを再読み込みします。

### 終了タグや引用符が抜けている

```html
<!-- 間違い -->
<a href="works.html>作品を見る</a>

<!-- 正しい -->
<a href="works.html">作品を見る</a>
```

### ファイルの場所が違う

`src="images/photo.jpg"`と書いた場合、HTMLファイルと同じ場所に`images`フォルダーが必要です。

### 大文字と小文字が一致していない

コードが`photo.jpg`、実際のファイルが`Photo.jpg`では、公開先によって画像を表示できないことがあります。

### idが存在しない、または重複している

`href="#top"`を使うなら、ページ内に`id="top"`が必要です。同じ`id`を複数の要素へ付けないようにします。

### 見た目のためにHTMLを選んでいる

大きな文字にするためだけに`h1`、余白のために`br`、枠線のために`border`属性を使わず、見た目はCSSで整えます。

---

## 15. 確認問題

1. HTMLは何を表すための言語ですか。
2. 要素、タグ、属性の違いを説明してください。
3. `head`と`body`には、それぞれ何を書きますか。
4. `h1`から`h6`の数字は何を表しますか。
5. `img`の`alt`属性は何のためにありますか。
6. `label`の`for`と`input`の`id`を同じ値にする理由は何ですか。
7. HTMLだけでフォームの入力内容を保存できますか。
8. 表をページのレイアウトに使わないほうがよいのはなぜですか。

<details>
<summary>解答例</summary>

1. Webページの内容と構造。
2. 要素は部品全体、タグは要素の始まりや終わりを示す記号、属性は要素へ追加情報を与える設定。
3. `head`にはページの設定や情報、`body`には利用者へ表示する内容を書く。
4. 見出しの階層と重要度。
5. 画像を見られない場合にも、その役割や内容を伝えるため。
6. ラベルと入力欄をプログラム上でも結び付け、読み上げやクリック操作をしやすくするため。
7. できない。保存や送信にはサーバー側の処理やフォームサービスなどが必要。
8. 表は行と列を持つデータのための要素であり、レイアウトに使うと文書構造が伝わりにくく、画面幅への対応も難しくなるため。

</details>

---

## まとめ

- HTMLはWebページの内容と構造を表すマークアップ言語
- 要素は正しく入れ子にし、属性値は引用符で囲む
- 見出し、段落、リストなどを内容の意味に合わせて使う
- 画像には役割に合う`alt`を付ける
- 表は行と列のデータ、フォームは利用者の入力に使う
- HTMLは見た目だけでなく、人や機械に意味を伝えるために書く
- フォームの送信・保存にはHTML以外の仕組みも必要

## 参考資料

- [元教材：HTMLのまとめ（Notion）](https://app.notion.com/p/323b4d03741180239f44f55e30912b45)
- [MDN Web Docs「Basic HTML syntax」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax)
- [MDN Web Docs「Structuring documents」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents)
- [MDN Web Docs「HTML table basics」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics)
- [MDN Web Docs「Forms and buttons in HTML」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_forms)
- [MDN Web Docs「HTML: A good basis for accessibility」](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML)
- [WHATWG HTML Living Standard](https://html.spec.whatwg.org/)

※外部サイトの内容やURLは変更されることがあります。
