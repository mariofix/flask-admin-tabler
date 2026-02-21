import typing
from dataclasses import dataclass

from flask_admin.theme import Theme


@dataclass
class TablerTheme(Theme):
    """
    Tabler 1.4.0 theme for Flask-Admin.

    Uses Tabler UI (https://tabler.io/) as the front end, loaded via CDN.

    Templates are provided by this example package and override Flask-Admin's
    blueprint templates via Flask's app-level template resolution.

    Usage::

        t = TablerTheme()
        admin = Admin(app, name='microblog', theme=t)

    Or with a custom base template::

        t = TablerTheme(base_template='my_base.html')
        admin = Admin(app, name='microblog', theme=t)
    """

    folder: typing.Literal["tabler"] = "tabler"
    base_template: str = "admin/base.html"
