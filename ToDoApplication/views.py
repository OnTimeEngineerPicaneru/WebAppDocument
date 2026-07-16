# ===================================================
# views.py - ビュー(画面表示)とルーティング(URL設定)のファイル
# ===================================================
# URL(例: /login, /home)と処理を結びつけることを「ルーティング」と呼ぶ。

from flask import (
    request,
    redirect,
    render_template,
    url_for,
    flash,
)
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, TaskList, TaskStatus
from app import app


LOGIN_ID_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 8
TASK_NAME_MAX_LENGTH = 100


def validate_login_id(login_id):
    """ログインIDを検証し、エラーメッセージを返す。"""
    if not login_id:
        return "ログインIDを入力してください"
    if not LOGIN_ID_MIN_LENGTH <= len(login_id) <= 100:
        return "ログインIDは3文字以上100文字以内で入力してください"
    return None


def validate_password(password):
    """パスワードを検証し、エラーメッセージを返す。"""
    if len(password) < PASSWORD_MIN_LENGTH:
        return "パスワードは8文字以上で入力してください"
    return None


def parse_task_form():
    """タスクフォームを検証し、タスク名・状態・エラーを返す。"""
    task_name = request.form.get("task_name", "").strip()
    status_name = request.form.get("status", "")

    if not task_name:
        return None, None, "タスク名を入力してください"
    if len(task_name) > TASK_NAME_MAX_LENGTH:
        return None, None, "タスク名は100文字以内で入力してください"
    if status_name not in TaskStatus.__members__:
        return None, None, "正しいステータスを選択してください"

    return task_name, TaskStatus[status_name], None


# ===================================================
# ログイン機能
# ===================================================
@app.route("/", methods=["GET", "POST"])
def login():
    """ログイン画面の表示とログイン処理"""
    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")

        user_data = User.query.filter_by(login_id=login_id).first()

        if user_data is not None and check_password_hash(user_data.password, password):
            login_user(user_data)
            return redirect(url_for("home"))

        flash("ログインIDまたはパスワードが正しくありません", "danger")

    return render_template("login.html")


# ===================================================
# ユーザ登録画面
# ===================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    """ユーザー登録画面の表示と新規ユーザー登録処理"""
    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")

        error = validate_login_id(login_id) or validate_password(password)
        if error:
            flash(error, "danger")
            return render_template("register.html"), 400

        # パスワードは平文のまま保存せず、ハッシュ化してから保存する
        new_user_data = User(
            login_id=login_id, password=generate_password_hash(password)
        )

        db.session.add(new_user_data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("そのログインIDはすでに使用されています", "danger")
            return render_template("register.html"), 409

        return redirect(url_for("login"))

    return render_template("register.html")


# ===================================================
# タスク一覧(ホーム画面)
# ===================================================
@app.route("/home", methods=["GET"])
@login_required
def home():
    """ログイン中のユーザーが持つタスクを一覧表示する"""
    task_list = TaskList.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", task_list=task_list)


# ===================================================
# タスク追加
# ===================================================
@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    """タスク追加画面の表示と新規タスク登録処理"""
    if request.method == "POST":
        task_name, status, error = parse_task_form()
        if error:
            flash(error, "danger")
            return render_template("add_task.html"), 400

        add_data = TaskList(
            task_name=task_name,
            status=status,
            user_id=current_user.id,
        )

        db.session.add(add_data)
        try:
            db.session.commit()
        except IntegrityError:
            # (user_id, task_name)の複合ユニーク制約に違反した場合(タスク名の重複)
            db.session.rollback()
            flash(f"タスク「{task_name}」はすでに登録されています", "danger")
        else:
            flash(f"タスク「{task_name}」を登録しました", "success")
            return redirect(url_for("home"))

    return render_template("add_task.html")


# ===================================================
# タスク削除
# ===================================================
@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    """指定されたIDのタスクを削除する(自分のタスクのみ削除可能)"""
    task = TaskList.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash("他のユーザーのタスクは削除できません", "danger")
        return redirect(url_for("home"))

    db.session.delete(task)
    db.session.commit()

    flash(f"タスク「{task.task_name}」を削除しました", "success")
    return redirect(url_for("home"))


# ===================================================
# タスク編集
# ===================================================
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    """指定されたIDのタスクを編集する(自分のタスクのみ編集可能)"""
    task = TaskList.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash("他のユーザーのタスクは編集できません", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        task_name, status, error = parse_task_form()
        if error:
            flash(error, "danger")
            return render_template("edit_task.html", task=task), 400

        task.task_name = task_name
        task.status = status
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f"タスク「{task_name}」はすでに登録されています", "danger")
            return render_template("edit_task.html", task=task), 409

        flash(f"タスク「{task.task_name}」を更新しました", "success")
        return redirect(url_for("home"))

    return render_template("edit_task.html", task=task)


# ===================================================
# ログアウト
# ===================================================
@app.post("/logout")
@login_required
def logout():
    """ユーザーをログアウトさせる"""
    logout_user()
    flash("ログアウトしました", "info")
    return redirect(url_for("login"))
