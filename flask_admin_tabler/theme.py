import typing
from dataclasses import dataclass

from flask import Blueprint
from flask import Flask
from flask_admin.theme import Theme


@dataclass
class TablerTheme(Theme):
    """
    Tabler theme for Flask-Admin.

    Uses Tabler UI (https://tabler.io/) as the front end, loaded via CDN.

    Templates live in ``flask_admin_tabler/templates/tabler/`` which matches
    ``Theme.folder = "tabler"``.  Registering the package blueprint **before**
    Flask-Admin's admin blueprint ensures our templates are resolved first by
    Flask's template loader.

    Usage::

        from flask_admin_tabler import TablerTheme

        theme = TablerTheme()
        theme.init_app(app)  # call before Admin(app, ...)
        admin = Admin(app, name="my app", theme=theme)

    Or with a sidebar layout and dark color scheme::

        theme = TablerTheme(layout="vertical", color_scheme="dark")
        theme.init_app(app)
        admin = Admin(app, name="my app", theme=theme)

    Parameters
    ----------
    layout:
        ``"horizontal"`` (default) renders a top navigation bar.
        ``"vertical"`` renders a sidebar navigation panel.
    color_scheme:
        ``"light"`` (default) uses the light Tabler theme.
        ``"dark"`` applies ``data-bs-theme="dark"`` to the ``<html>`` element.
    tabler_icons:
        When ``True`` (default) the Tabler Icons web-font CSS is loaded from
        CDN.  Set to ``False`` to skip loading it.
    """

    folder: typing.Literal["tabler"] = "tabler"
    base_template: str = "admin/base.html"
    tabler_icons: bool = True
    layout: typing.Literal["horizontal", "vertical"] = "horizontal"
    color_scheme: typing.Literal["light", "dark"] = "light"

    def init_app(self, app: Flask) -> None:
        """Register Tabler theme templates and static files with the Flask app.

        Must be called *before* creating the ``Admin`` instance.  Flask
        resolves blueprint templates in registration order, so registering
        this blueprint first guarantees our Tabler templates take priority
        over Flask-Admin's default Bootstrap ones.
        """
        bp = Blueprint(
            "flask_admin_tabler",
            __name__,
            template_folder="templates/tabler",
            static_folder="static",
            static_url_path="/static/flask_admin_tabler",
        )
        app.register_blueprint(bp)
