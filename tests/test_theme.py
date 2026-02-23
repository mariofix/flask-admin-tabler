import pytest
from flask import Flask
from flask_admin import Admin
from flask_admin_tabler import TablerTheme


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True
    return app


def test_theme_defaults():
    theme = TablerTheme()
    assert theme.folder == "tabler"
    assert theme.base_template == "admin/base.html"
    assert theme.tabler_icons is True
    assert theme.layout == "horizontal"
    assert theme.color_scheme == "light"
    assert theme.primary_color is None
    assert theme.font is None
    assert theme.base_color is None
    assert theme.corner_radius is None


def test_theme_custom_base_template():
    theme = TablerTheme(base_template="my_base.html")
    assert theme.base_template == "my_base.html"


def test_theme_tabler_icons_disabled():
    theme = TablerTheme(tabler_icons=False)
    assert theme.tabler_icons is False


def test_theme_layout_vertical():
    theme = TablerTheme(layout="vertical")
    assert theme.layout == "vertical"


def test_theme_color_scheme_dark():
    theme = TablerTheme(color_scheme="dark")
    assert theme.color_scheme == "dark"


def test_init_app_registers_blueprint(app):
    theme = TablerTheme()
    theme.init_app(app)
    assert "flask_admin_tabler" in app.blueprints


def test_init_app_static_url(app):
    theme = TablerTheme()
    theme.init_app(app)
    with app.test_request_context():
        from flask import url_for

        url = url_for(
            "flask_admin_tabler.static", filename="admin/css/tabler/admin.css"
        )
        assert "flask_admin_tabler" in url
        assert "admin.css" in url


def test_admin_index_renders_tabler(app):
    theme = TablerTheme()
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    # Tabler CSS is loaded from CDN
    assert b"tabler" in response.data


def test_admin_uses_tabler_base_template(app):
    theme = TablerTheme()
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    # Tabler CDN link is present
    assert b"cdn.jsdelivr.net/npm/@tabler" in response.data
    # Bootstrap CDN should NOT be present (we replaced it)
    assert b"bootstrap.min.css" not in response.data


def test_admin_tabler_icons_css_loaded_by_default(app):
    theme = TablerTheme()
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"tabler-icons.min.css" in response.data


def test_admin_tabler_icons_css_not_loaded_when_disabled(app):
    theme = TablerTheme(tabler_icons=False)
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"tabler-icons.min.css" not in response.data


def test_admin_font_awesome_css_loaded_when_tabler_icons_disabled(app):
    theme = TablerTheme(tabler_icons=False)
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"font-awesome" in response.data


def test_admin_font_awesome_css_not_loaded_when_tabler_icons_enabled(app):
    theme = TablerTheme(tabler_icons=True)
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"font-awesome" not in response.data


def test_admin_horizontal_layout_renders_navbar(app):
    theme = TablerTheme(layout="horizontal")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    # Horizontal layout uses a top navbar header
    assert b"navbar-expand-md" in response.data
    # Sidebar element should NOT be present
    assert b"navbar-vertical" not in response.data


def test_admin_vertical_layout_renders_sidebar(app):
    theme = TablerTheme(layout="vertical")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    # Vertical layout uses a sidebar aside element
    assert b"navbar-vertical" in response.data
    # sidebar-menu collapse target should be present
    assert b"sidebar-menu" in response.data


def test_admin_dark_color_scheme_sets_data_attribute(app):
    theme = TablerTheme(color_scheme="dark")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b'data-bs-theme="dark"' in response.data


def test_admin_light_color_scheme_no_dark_attribute(app):
    theme = TablerTheme(color_scheme="light")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    # Light mode sets data-bs-theme="light", never "dark"
    assert b'data-bs-theme="light"' in response.data
    assert b'data-bs-theme="dark"' not in response.data


def test_theme_primary_color_sets_attribute(app):
    theme = TablerTheme(primary_color="indigo")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b'data-bs-theme-primary="indigo"' in response.data


def test_theme_primary_color_none_omits_attribute(app):
    theme = TablerTheme()
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"data-bs-theme-primary" not in response.data


def test_theme_font_sets_attribute(app):
    theme = TablerTheme(font="serif")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b'data-bs-theme-font="serif"' in response.data


def test_theme_base_color_sets_attribute(app):
    theme = TablerTheme(base_color="slate")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b'data-bs-theme-base="slate"' in response.data


def test_theme_corner_radius_sets_attribute(app):
    theme = TablerTheme(corner_radius="1.5")
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b'data-bs-theme-radius="1.5"' in response.data


def test_theme_corner_radius_none_omits_attribute(app):
    theme = TablerTheme()
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"data-bs-theme-radius" not in response.data


def test_theme_all_settings_rendered(app):
    theme = TablerTheme(
        color_scheme="dark",
        primary_color="teal",
        font="monospace",
        base_color="zinc",
        corner_radius="2",
    )
    theme.init_app(app)
    Admin(app, name="Test Admin", theme=theme)

    client = app.test_client()
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b'data-bs-theme="dark"' in response.data
    assert b'data-bs-theme-primary="teal"' in response.data
    assert b'data-bs-theme-font="monospace"' in response.data
    assert b'data-bs-theme-base="zinc"' in response.data
    assert b'data-bs-theme-radius="2"' in response.data


def test_theme_invalid_primary_color_raises():
    import pytest

    with pytest.raises(ValueError, match="primary_color"):
        TablerTheme(primary_color="invalid-color")


def test_theme_invalid_corner_radius_raises():
    import pytest

    with pytest.raises(ValueError, match="corner_radius"):
        TablerTheme(corner_radius="3")
