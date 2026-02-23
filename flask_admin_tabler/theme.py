import typing
from dataclasses import dataclass

from flask import Blueprint
from flask import Flask
from flask_admin.theme import Theme

_PRIMARY_COLORS = ("blue", "azure", "indigo", "purple", "pink", "red", "orange", "yellow", "lime", "green", "teal", "cyan")
_FONT_VALUES = ("sans-serif", "serif", "monospace", "comic")
_BASE_VALUES = ("slate", "gray", "zinc", "neutral", "stone")
_RADIUS_VALUES = ("0", "0.5", "1", "1.5", "2")


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

    Or with a sidebar, dark scheme, blue accent, and rounded corners::

        theme = TablerTheme(
            layout="vertical",
            color_scheme="dark",
            primary_color="blue",
            font="sans-serif",
            base_color="gray",
            corner_radius="1.5",
        )
        theme.init_app(app)
        admin = Admin(app, name="my app", theme=theme)

    Parameters
    ----------
    layout:
        ``"horizontal"`` (default) renders a top navigation bar.
        ``"vertical"`` renders a sidebar navigation panel.
    color_scheme:
        ``"light"`` (default) or ``"dark"``.  Sets ``data-bs-theme`` on
        the ``<html>`` element.
    primary_color:
        Accent color for the theme.  Sets ``data-bs-theme-primary`` on
        the ``<html>`` element.  One of ``"blue"`` (default), ``"azure"``,
        ``"indigo"``, ``"purple"``, ``"pink"``, ``"red"``, ``"orange"``,
        ``"yellow"``, ``"lime"``, ``"green"``, ``"teal"``, ``"cyan"``.
        ``None`` (default) leaves the attribute unset, which falls back to
        Tabler's default (blue).
    font:
        Font family for the theme.  Sets ``data-bs-theme-font`` on the
        ``<html>`` element.  One of ``"sans-serif"`` (default), ``"serif"``,
        ``"monospace"``, ``"comic"``.  ``None`` leaves the attribute unset.
    base_color:
        Gray shade for the theme.  Sets ``data-bs-theme-base`` on the
        ``<html>`` element.  One of ``"slate"``, ``"gray"`` (default),
        ``"zinc"``, ``"neutral"``, ``"stone"``.  ``None`` leaves the
        attribute unset.
    corner_radius:
        Border-radius scale factor.  Sets ``data-bs-theme-radius`` on the
        ``<html>`` element.  One of ``"0"``, ``"0.5"``, ``"1"`` (default),
        ``"1.5"``, ``"2"``.  ``None`` leaves the attribute unset.
    tabler_icons:
        When ``True`` (default) the Tabler Icons web-font CSS is loaded from
        CDN.  Set to ``False`` to skip loading it.
    """

    folder: typing.Literal["tabler"] = "tabler"
    base_template: str = "admin/base.html"
    tabler_icons: bool = True
    layout: typing.Literal["horizontal", "vertical"] = "horizontal"
    color_scheme: typing.Literal["light", "dark"] = "light"
    primary_color: typing.Optional[str] = None
    font: typing.Optional[str] = None
    base_color: typing.Optional[str] = None
    corner_radius: typing.Optional[str] = None

    def __post_init__(self) -> None:
        if self.primary_color is not None and self.primary_color not in _PRIMARY_COLORS:
            raise ValueError(f"primary_color must be one of {_PRIMARY_COLORS}, got {self.primary_color!r}")
        if self.font is not None and self.font not in _FONT_VALUES:
            raise ValueError(f"font must be one of {_FONT_VALUES}, got {self.font!r}")
        if self.base_color is not None and self.base_color not in _BASE_VALUES:
            raise ValueError(f"base_color must be one of {_BASE_VALUES}, got {self.base_color!r}")
        if self.corner_radius is not None and self.corner_radius not in _RADIUS_VALUES:
            raise ValueError(f"corner_radius must be one of {_RADIUS_VALUES}, got {self.corner_radius!r}")

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
