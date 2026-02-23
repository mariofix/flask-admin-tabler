"""
Full theme settings example – flask-admin-tabler
=================================================

Demonstrates every visual setting available in ``TablerTheme``:

- ``layout``        — sidebar or top navbar
- ``color_scheme``  — light or dark
- ``primary_color`` — accent color
- ``font``          — font family
- ``base_color``    — gray shade
- ``corner_radius`` — border-radius factor

All settings are applied server-side as ``data-bs-*`` HTML attributes on the
``<html>`` element.  No JavaScript or localStorage is involved.

Run::

    pip install flask-admin-tabler flask-sqlalchemy
    python examples/theme_settings.py

Then open http://127.0.0.1:5000/admin/ in your browser.

Experiment by changing the values below and restarting the server.
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


# ── Theme settings ─────────────────────────────────────────────────────────────
#
# layout        : "horizontal" (top navbar, default) | "vertical" (sidebar)
# color_scheme  : "light" (default) | "dark"
# primary_color : "blue" (default) | "azure" | "indigo" | "purple" | "pink"
#                 "red" | "orange" | "yellow" | "lime" | "green" | "teal" | "cyan"
# font          : "sans-serif" (default) | "serif" | "monospace" | "comic"
# base_color    : "gray" (default) | "slate" | "zinc" | "neutral" | "stone"
# corner_radius : "1" (default) | "0" | "0.5" | "1.5" | "2"
#
# All optional settings default to None, which lets Tabler use its built-in
# defaults.  Invalid values raise ValueError at startup.
# ──────────────────────────────────────────────────────────────────────────────

theme = TablerTheme(
    layout="vertical",
    color_scheme="dark",
    primary_color="teal",
    font="sans-serif",
    base_color="gray",
    corner_radius="1.5",
)
theme.init_app(app)

admin = Admin(app, name="Theme Settings Demo", theme=theme)
admin.add_view(ModelView(User, db.session))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.first():
            db.session.add_all(
                [
                    User(username="alice", email="alice@example.com"),
                    User(username="bob", email="bob@example.com"),
                    User(username="charlie", email="charlie@example.com"),
                ]
            )
            db.session.commit()
    app.run()
