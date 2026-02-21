import pytest
from flask import Flask
from jinja2 import StrictUndefined

from flask_admin import Admin
from flask_admin import TablerTheme
from flask_admin.contrib.sqla.view import ModelView
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


@pytest.fixture
def tabler_admin(app, babel):
    admin = Admin(app, theme=TablerTheme())
    yield admin


def create_models(sqla_db_ext):
    class User(sqla_db_ext.Base):  # type: ignore[name-defined, misc]
        __tablename__ = "user"
        id = Column(Integer, primary_key=True)
        first_name = Column(String(20))
        last_name = Column(String(20))

        def __str__(self):
            return self.first_name

    class Post(sqla_db_ext.Base):  # type: ignore[name-defined, misc]
        __tablename__ = "post"
        id = Column(Integer, primary_key=True)
        title = Column(String(20))
        desc = Column(String(20))
        author_id = Column(Integer, ForeignKey("user.id"))
        author = relationship("User", backref=backref("posts", lazy="dynamic"))

    sqla_db_ext.create_all()

    return User, Post


def fill_data(sqla_db_ext, User, Post):
    u1 = User(first_name="user1", last_name="userdesc1")
    u2 = User(first_name="user2", last_name="userdesc2")

    sqla_db_ext.db.session.add_all(
        [
            u1,
            u2,
            Post(title="post1", desc="postdesc1", author=u1),
            Post(title="post2", desc="postdesc2", author=u2),
        ]
    )
    sqla_db_ext.db.session.commit()


def test_tabler_theme_index(app, sqla_db_ext, tabler_admin):
    with app.app_context():
        client = app.test_client()
        response = client.get("/admin/")
        assert response.status_code == 200
        data = response.data.decode("utf-8")

        # Check that Tabler CDN assets are loaded
        assert "tabler/core@1.4.0" in data
        # Check that the Tabler page structure is present
        assert "page-wrapper" in data


def test_tabler_theme_list_view(app, sqla_db_ext, tabler_admin):
    with app.app_context():
        User, Post = create_models(sqla_db_ext)
        fill_data(sqla_db_ext, User, Post)

        class PostView(ModelView):
            column_list = ["title", "author.first_name"]

        tabler_admin.add_view(PostView(Post, sqla_db_ext.db))

        client = app.test_client()
        response = client.get("/admin/post/")
        data = response.data.decode("utf-8")
        assert response.status_code == 200

        # Check that Tabler table classes are present
        assert "table table-vcenter table-striped table-bordered table-hover" in data

        # Check that custom column classes are applied
        assert "column-header col-title" in data
        assert "column-header col-author-first_name" in data

        # Check Tabler CDN is referenced
        assert "tabler/core@1.4.0" in data


def test_tabler_theme_navbar(app, sqla_db_ext, tabler_admin):
    with app.app_context():
        client = app.test_client()
        response = client.get("/admin/")
        assert response.status_code == 200
        data = response.data.decode("utf-8")

        # Check that Tabler navbar is rendered with Bootstrap 5 data attributes
        assert "data-bs-toggle" in data
        assert "navbar-expand-md" in data
