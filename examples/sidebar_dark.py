"""
Sidebar + dark mode example – flask-admin-tabler
=================================================

Demonstrates the vertical (sidebar) layout with dark color scheme.

Run::

    pip install flask-admin-tabler flask-sqlalchemy
    python examples/sidebar_dark.py

Then open http://127.0.0.1:5000/admin/ in your browser.
"""

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin_tabler import TablerTheme
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"  # replace with a secure random value in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"  # in-memory database

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"


# Sidebar layout with dark mode
theme = TablerTheme(
    layout="vertical",   # left sidebar instead of top navbar
    color_scheme="dark", # dark mode
)
theme.init_app(app)

admin = Admin(app, name="Sidebar Dark", theme=theme)
admin.add_view(ModelView(User, db.session, category="Content"))
admin.add_view(ModelView(Post, db.session, category="Content"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.first():
            db.session.add_all(
                [
                    User(username="alice", email="alice@example.com"),
                    User(username="bob", email="bob@example.com"),
                ]
            )
            db.session.add_all(
                [
                    Post(title="Hello World", body="First post content."),
                    Post(title="Second Post", body="Another post."),
                ]
            )
            db.session.commit()
    app.run()
