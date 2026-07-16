# ===================================================
# models.py - データベースモデル定義ファイル
# ===================================================
# SQLAlchemyを使って、テーブル構造をPythonのクラスとして定義する。

from flask_sqlalchemy import SQLAlchemy  # データベース操作用
from flask_login import UserMixin  # ログイン機能で必要なユーザークラスの基本機能
from datetime import datetime, timezone, timedelta
import enum

db = SQLAlchemy()


class TaskStatus(enum.Enum):
    """タスクのステータス。Enumにすることで決まった値しか使えないようにする"""

    NOT_STARTED = "未達成"
    IN_PROGRESS = "進行中"
    COMPLETED = "実施済み"
    PENDING = "保留中"


class User(UserMixin, db.Model):
    """ユーザー情報を管理するモデル

    UserMixinを継承することで、Flask-Loginに必要な機能が自動的に追加される。
    """

    __tablename__ = "user_master"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # login_id: ログインに使用するID(重複不可)
    login_id = db.Column(db.String(100), nullable=False, unique=True, index=True)

    # password: ハッシュ化した値を保存する(平文では保存しない)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # ユーザーを削除したら、そのユーザーのタスクも連鎖して削除する
    tasks = db.relationship(
        "TaskList", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.login_id}>"


class TaskList(db.Model):
    """タスク情報を管理するモデル"""

    __tablename__ = "task_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100), nullable=False)
    status = db.Column(
        db.Enum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED
    )

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # user_id: このタスクを所有するユーザーのID(外部キー)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_master.id"), nullable=False, index=True
    )

    # 同じユーザーが同じ名前のタスクを複数作れないようにする複合ユニーク制約
    __table_args__ = (
        db.UniqueConstraint("user_id", "task_name", name="_user_task_unique"),
    )

    @property
    def created_at_jst(self):
        """created_at(UTC)を日本時間(JST, UTC+9)の文字列に変換して返す"""
        jst = timezone(timedelta(hours=9))
        return (
            self.created_at.replace(tzinfo=timezone.utc)
            .astimezone(jst)
            .strftime("%Y年%m月%d日 %H:%M")
        )

    def __repr__(self):
        return f"<TaskList {self.task_name} - {self.status.value}>"
