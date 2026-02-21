import datetime
import os.path as op

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from examples.flask_admin_tabler.theme import TablerTheme

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "secret"
app.config["DATABASE_FILE"] = "db.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE_FILE"]
app.config["SQLALCHEMY_ECHO"] = False

db = SQLAlchemy(app)

admin = Admin(
    app,
    name="Example: Tabler",
    theme=TablerTheme(),
)


@app.route("/")
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

    def __repr__(self):
        return self.name


class Page(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    content: Mapped[Text] = mapped_column(Text)

    def __repr__(self):
        return self.title


class UserAdmin(ModelView):
    column_searchable_list = ("name",)
    column_filters = ("name", "email")
    can_export = True


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    admin.add_view(UserAdmin(User, db, name="Users"))
    admin.add_view(ModelView(Page, db, name="Pages"))

    app_dir = op.realpath(op.dirname(__file__))
    database_path = op.join(app_dir, app.config["DATABASE_FILE"])
    if not op.exists(database_path):
        with app.app_context():
            db.create_all()

    app.run(debug=True)
