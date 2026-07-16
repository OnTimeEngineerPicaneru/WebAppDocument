# Pythonの例外処理

プログラムを実行していると、入力された値が想定と違う、ファイルが存在しない、0で割ろうとしたなど、通常の処理を続けられない状況が発生します。Pythonでは、このような状況を**例外（Exception）**として扱います。

例外処理を使うと、発生する可能性が分かっている問題へ対応し、利用者に分かりやすいメッセージを表示したり、必要な後片付けを行ったりできます。

---

## 1. 構文エラーと例外の違い

Pythonのエラーは、大きく「構文エラー」と「例外」に分けて考えられます。

### 構文エラー

Pythonの文法に誤りがあり、プログラムを正しく読み取れない状態です。

```python
if score >= 60
    print("合格")
```

`if`文の末尾に`:`がないため、次のようなエラーになります。

```text
SyntaxError: expected ':'
```

構文エラーは、基本的にコードを修正する必要があります。通常の`try`文で囲んで、実行中の問題として処理するものではありません。

### 例外

文法は正しくても、実行中の値や状況によって処理を続けられなくなることがあります。

```python
number = int("abc")
```

`"abc"`は整数へ変換できないため、実行すると`ValueError`が発生します。

```text
ValueError: invalid literal for int() with base 10: 'abc'
```

発生する可能性を予想できる例外は、`try`と`except`で処理できます。

---

## 2. トレースバックの読み方

処理されなかった例外が発生すると、Pythonは**トレースバック**を表示します。

```python
def divide(a, b):
    return a / b


result = divide(10, 0)
print(result)
```

実行結果の例：

```text
Traceback (most recent call last):
  File "app.py", line 5, in <module>
    result = divide(10, 0)
  File "app.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
```

トレースバックは、下から上へ確認すると原因を見つけやすくなります。

1. 最後の行で例外の種類と説明を確認する
2. その上の行で、例外が発生したコードを確認する
3. 必要に応じて、さらに上へたどって呼び出し元を確認する

この例では、`a / b`で`b`が0だったため、`ZeroDivisionError`が発生しています。

---

## 3. tryとexcept

例外を処理する基本形です。

```python
try:
    # 例外が発生する可能性のある処理
except 例外の種類:
    # 指定した例外が発生した場合の処理
```

例：入力された文字列を整数へ変換します。

```python
text = input("整数を入力してください: ")

try:
    number = int(text)
except ValueError:
    print("整数として読み取れませんでした。")
```

処理の流れは次のとおりです。

```text
try内を実行
  ├─ 例外が発生しない → exceptを飛ばす
  └─ ValueErrorが発生 → tryの残りを中止してexceptを実行
```

`except ValueError`は、`ValueError`だけを処理します。それ以外の例外は処理されず、さらに外側の処理へ伝わります。

---

## 4. 複数の例外を処理する

発生する問題ごとに処理を分けられます。

```python
try:
    number = int(input("割る数を入力してください: "))
    result = 10 / number
except ValueError:
    print("整数を入力してください。")
except ZeroDivisionError:
    print("0で割ることはできません。")
```

上から順番に確認され、最初に一致した`except`だけが実行されます。

### 複数の例外を同じ処理にする

同じ対応でよい場合は、例外をタプルで指定できます。

```python
try:
    value = data[index]
except (IndexError, TypeError):
    print("データまたは番号を確認してください。")
```

### 例外オブジェクトを受け取る

`as`を使うと、例外が持つ詳しい情報を受け取れます。

```python
try:
    number = int("abc")
except ValueError as error:
    print(f"変換に失敗しました: {error}")
```

利用者向けの画面には分かりやすい文章を表示し、詳しい例外情報は開発者向けのログへ記録するのが一般的です。例外メッセージには、ファイルパスや内部情報が含まれることがあるため、そのまま公開画面へ表示しないようにします。

---

## 5. else

`else`は、`try`で例外が発生しなかった場合だけ実行されます。

```python
try:
    number = int(input("整数を入力してください: "))
except ValueError:
    print("整数ではありません。")
else:
    print(f"入力された整数は{number}です。")
```

成功後の処理を`try`の中へすべて書くこともできますが、`else`へ分けると`try`の範囲を小さくできます。

```python
try:
    number = int(text)
except ValueError:
    print("変換できませんでした。")
else:
    save_number(number)
```

この形なら、`save_number()`で別の例外が発生しても、整数変換用の`except ValueError`が誤って処理する可能性を減らせます。

---

## 6. finally

`finally`は、例外が発生したかどうかに関係なく、最後に実行されます。

```python
try:
    number = int(input("整数を入力してください: "))
except ValueError:
    print("整数ではありません。")
else:
    print(f"入力値: {number}")
finally:
    print("入力処理を終了します。")
```

`finally`は、外部リソースの解放や一時的な状態の後片付けなどに使います。

```python
connection = open_connection()

try:
    connection.send("Hello")
finally:
    connection.close()
```

ただし、ファイルなどのようにコンテキストマネージャーを利用できるものは、後述する`with`を優先します。

### finallyでreturnしない

`finally`の中に`return`、`break`、`continue`を書くと、処理されていない例外や別の戻り値を隠すことがあります。動作が分かりにくくなるため避けます。

```python
# 避けたい例
def calculate():
    try:
        return 10 / 0
    finally:
        return 0
```

このコードでは、`ZeroDivisionError`が`finally`の`return`によって隠れてしまいます。

---

## 7. try文の組み合わせ

`try`文には、目的に応じていくつかの組み合わせがあります。

```python
try:
    処理
except ValueError:
    例外処理
```

```python
try:
    処理
except ValueError:
    例外処理
else:
    成功した場合の処理
finally:
    必ず行う後片付け
```

`try`と`finally`だけを組み合わせることもできます。この場合、例外を処理するのではなく、後片付けをしてから例外を外側へ伝えます。

```python
try:
    処理
finally:
    後片付け
```

---

## 8. 代表的な標準例外

### 値と型

| 例外 | 発生例 | 意味 |
| --- | --- | --- |
| `ValueError` | `int("abc")` | 型は受け付けられるが、値が不適切 |
| `TypeError` | `"年齢: " + 15` | 演算や関数に対して型が不適切 |

```python
try:
    age = int("十五")
except ValueError:
    print("数字で入力してください。")
```

```python
try:
    message = "年齢: " + 15
except TypeError:
    print("文字列と整数をそのまま連結できません。")
```

### 数値計算

| 例外 | 発生例 | 意味 |
| --- | --- | --- |
| `ZeroDivisionError` | `10 / 0` | 0で除算または剰余計算をした |
| `OverflowError` | 処理可能な範囲を超える計算 | 数値計算の結果が大きすぎる |

```python
try:
    average = total / count
except ZeroDivisionError:
    print("データがないため平均を計算できません。")
```

### リストと辞書

| 例外 | 発生例 | 意味 |
| --- | --- | --- |
| `IndexError` | `[10, 20][5]` | 存在しない位置を参照した |
| `KeyError` | `user["email"]` | 辞書に存在しないキーを参照した |

```python
items = ["HTML", "CSS"]

try:
    print(items[5])
except IndexError:
    print("指定された位置にデータがありません。")
```

辞書のキーがなくても問題ない場合は、例外処理ではなく`get()`が適しています。

```python
user = {"name": "さくら"}
email = user.get("email", "未登録")
print(email)
```

### 名前と属性

| 例外 | 発生例 | 意味 |
| --- | --- | --- |
| `NameError` | 未定義の変数を使う | 名前が見つからない |
| `AttributeError` | 存在しない属性を参照 | オブジェクトに属性がない |

`NameError`や`AttributeError`は、入力の問題よりもコードの間違いで発生することがよくあります。むやみに処理して隠すのではなく、原因となるコードを修正します。

### ファイルとOS

| 例外 | 発生例 | 意味 |
| --- | --- | --- |
| `FileNotFoundError` | 存在しないファイルを開く | ファイルやフォルダーが見つからない |
| `PermissionError` | 権限のないファイルを開く | 操作する権限がない |
| `OSError` | OSに関係する処理の失敗 | ファイルや入出力などの広い問題 |

```python
try:
    with open("settings.txt", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("設定ファイルが見つかりません。")
except PermissionError:
    print("設定ファイルを読む権限がありません。")
```

`FileNotFoundError`と`PermissionError`は`OSError`の子クラスです。具体的な例外を先に書き、広い例外を後に書きます。

```python
try:
    read_settings()
except FileNotFoundError:
    print("ファイルがありません。")
except OSError:
    print("ファイル操作に失敗しました。")
```

### モジュールの読み込み

| 例外 | 意味 |
| --- | --- |
| `ModuleNotFoundError` | 指定したモジュールが見つからない |
| `ImportError` | モジュールや名前の読み込みに失敗した |

`ModuleNotFoundError`は`ImportError`の子クラスです。パッケージのインストール忘れ、仮想環境の選択間違い、ファイル名の衝突などを確認します。

---

## 9. 例外を発生させるraise

`raise`を使うと、条件に応じて自分で例外を発生させられます。

```python
def set_age(age):
    if age < 0:
        raise ValueError("年齢は0以上にしてください。")

    return age
```

```python
try:
    age = set_age(-1)
except ValueError as error:
    print(error)
```

関数が正しい結果を返せない場合に例外を発生させると、呼び出し側へ問題を明確に伝えられます。

### 同じ例外をもう一度発生させる

例外を記録してから外側へ伝えたい場合は、引数なしの`raise`を使います。

```python
import logging


try:
    save_data()
except OSError:
    logging.exception("データの保存に失敗しました。")
    raise
```

`raise error`と書くより、引数なしの`raise`を使う方が、元のトレースバックを保ったまま再送出できます。

---

## 10. 独自の例外

アプリ独自の問題を標準例外だけでは表しにくい場合は、独自の例外クラスを作れます。

```python
class InsufficientBalanceError(Exception):
    """残高不足を表す例外。"""


def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("金額は1円以上にしてください。")

    if amount > balance:
        shortage = amount - balance
        raise InsufficientBalanceError(
            f"残高が{shortage}円不足しています。"
        )

    return balance - amount
```

```python
try:
    new_balance = withdraw(1000, 5000)
except ValueError as error:
    print(f"入力エラー: {error}")
except InsufficientBalanceError as error:
    print(f"取引を中止しました: {error}")
else:
    print(f"残高は{new_balance}円です。")
```

独自例外は通常、`Exception`を直接または間接的に継承し、クラス名の末尾を`Error`にします。

---

## 11. 例外の連鎖

低い階層で発生した例外を、アプリの意味に合う例外へ変換したいことがあります。`raise ... from ...`を使うと、元の原因を残したまま新しい例外を発生させられます。

```python
class SettingsError(Exception):
    """設定の読み込み失敗を表す例外。"""


def load_settings():
    try:
        with open("settings.txt", encoding="utf-8") as file:
            return file.read()
    except OSError as error:
        raise SettingsError(
            "設定を読み込めませんでした。"
        ) from error
```

トレースバックには、`OSError`が`SettingsError`の直接の原因であることが表示されます。利用者にはアプリに合った説明を提示しながら、開発者は元の原因も調査できます。

元の例外をトレースバックへ表示したくない特別な場合は`raise ... from None`も使えますが、原因調査が難しくなるため、理由がある場合だけ使用します。

---

## 12. withによる後片付け

ファイルは、`finally`で閉じるより`with`を使う方が簡潔で安全です。

```python
file = open("message.txt", encoding="utf-8")

try:
    content = file.read()
finally:
    file.close()
```

同じ処理を`with`で書くと次のようになります。

```python
with open("message.txt", encoding="utf-8") as file:
    content = file.read()
```

処理中に例外が発生しても、`with`ブロックを抜けるときにファイルが閉じられます。

`with`は例外をすべて無視する仕組みではありません。ファイルを閉じるなどの後片付けを行い、処理されていない例外は通常どおり外側へ伝えます。

---

## 13. 例外処理と条件分岐の使い分け

すべての問題を例外処理で解決する必要はありません。

### 条件で簡単に確認できる場合

```python
if count == 0:
    print("データがありません。")
else:
    print(total / count)
```

### 実行してみないと結果が分からない場合

ファイルは確認直後に削除される可能性もあります。存在確認と読み込みを分けるより、読み込みを試して例外を処理する方が確実です。

```python
try:
    with open("data.txt", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("ファイルが見つかりません。")
```

辞書の任意項目には`get()`、数値変換には`try`と`except ValueError`など、目的に合う方法を選びます。

---

## 14. 例外処理を書くときの注意

### 具体的な例外を指定する

```python
# 避けたい例
try:
    process_data()
except:
    print("失敗しました。")
```

例外の種類を省略した裸の`except:`は、`KeyboardInterrupt`や`SystemExit`などまで処理してしまいます。通常は具体的な例外を指定します。

```python
try:
    process_data()
except ValueError:
    print("データの値が正しくありません。")
```

### Exceptionを広く処理しすぎない

`except Exception`は、多くの通常の例外をまとめて処理します。アプリの一番外側でログを残す場合などには使えますが、どこにでも書くとプログラムの不具合まで隠してしまいます。

```python
try:
    run_application()
except Exception:
    logging.exception("予期しない問題が発生しました。")
    raise
```

### tryの範囲を小さくする

```python
# 範囲が広すぎる例
try:
    number = int(text)
    result = calculate(number)
    save(result)
except ValueError:
    print("値に問題があります。")
```

どの処理が`ValueError`を発生させたのか分かりにくくなります。想定している処理だけを`try`へ入れます。

```python
try:
    number = int(text)
except ValueError:
    print("整数を入力してください。")
else:
    result = calculate(number)
    save(result)
```

### passで問題を隠さない

```python
# 理由なく無視しない
try:
    save_data()
except OSError:
    pass
```

例外を意図的に無視する場合は、その理由が明確でなければなりません。通常は再試行、代替処理、ログ記録、利用者への通知などを行います。

### エラー内容をログへ残す

```python
import logging


try:
    update_database()
except OSError:
    logging.exception("データベース更新に失敗しました。")
    raise
```

`logging.exception()`は`except`ブロックの中で使うと、例外情報とトレースバックを記録します。本番環境では`print()`だけに頼らず、ログの保存場所や個人情報の扱いも決めます。

---

## 15. Flaskでの例外処理

Flaskでは、利用者の入力ミスとサーバー内部の不具合を分けて考えます。

```python
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/divide")
def divide():
    try:
        left = int(request.args.get("left", ""))
        right = int(request.args.get("right", ""))
        result = left / right
    except ValueError:
        return render_template(
            "divide.html",
            error="整数を入力してください。",
        ), 400
    except ZeroDivisionError:
        return render_template(
            "divide.html",
            error="0で割ることはできません。",
        ), 400

    return render_template("divide.html", result=result)
```

入力値が不正な場合は、利用者向けの説明と適切なHTTPステータスコードを返します。一方、予期していない例外をすべて握りつぶして「入力エラー」にしてはいけません。内部の不具合はログへ記録し、開発者が修正できる状態を保ちます。

公開環境ではデバッグ画面を利用者へ表示しません。トレースバックにはソースコード、ファイルパス、設定値などが含まれる可能性があります。

---

## 16. 例外処理の流れ

次のコードには、`try`、`except`、`else`、`finally`がすべて含まれています。

```python
def calculate_average(total_text, count_text):
    try:
        total = int(total_text)
        count = int(count_text)
        average = total / count
    except ValueError:
        print("整数へ変換できませんでした。")
        return None
    except ZeroDivisionError:
        print("個数を0にはできません。")
        return None
    else:
        print("平均を計算できました。")
        return average
    finally:
        print("計算処理を終了します。")
```

| 状況 | except | else | finally |
| --- | --- | --- | --- |
| 正常に計算できた | 実行しない | 実行する | 実行する |
| 整数へ変換できない | `ValueError`を実行 | 実行しない | 実行する |
| 0で割った | `ZeroDivisionError`を実行 | 実行しない | 実行する |
| 対応していない例外 | 実行しない | 実行しない | 実行後、例外が外へ伝わる |

---

## まとめ

- 構文エラーはPythonの文法上の誤り、例外はおもに実行中に発生する問題
- トレースバックの最後には例外の種類と説明が表示される
- `try`に例外が予想される処理、`except`に対応を書く
- `else`は例外がなかった場合、`finally`は最後に必ず実行される
- `raise`で意図的に例外を発生させられる
- 独自例外は通常`Exception`を継承する
- ファイルなどの後片付けには、利用できる場合は`with`を使う
- 具体的な例外を処理し、`try`の範囲を小さくする
- 予期しない例外を隠さず、開発者向けのログへ記録する

---

## 参考資料

### 元教材

- [Pythonの例外について](https://app.notion.com/p/340b4d037411800a962ec8503a2d7d98)

### 公式資料

- [Python公式チュートリアル：エラーと例外](https://docs.python.org/ja/3/tutorial/errors.html)
- [Python公式ドキュメント：組み込み例外](https://docs.python.org/ja/3/library/exceptions.html)
