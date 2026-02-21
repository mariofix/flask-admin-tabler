import typing
from dataclasses import dataclass
from functools import partial


@dataclass
class Theme:
    folder: str  # The templates folder name to use
    base_template: str


@dataclass
class BootstrapTheme(Theme):
    """
    Bootstrap theme for Flask-Admin.

    Usage::

        t = Bootstrap4Theme(
            base_template='my_base.html', # relative your templates folder
            swatch='cerulean',
            fluid=True
        )
        admin = Admin(app, name='microblog', theme=t)
    """

    folder: typing.Literal["bootstrap4"]
    base_template: str = "admin/base.html"
    swatch: str = "default"
    fluid: bool = False


Bootstrap4Theme = partial(BootstrapTheme, folder="bootstrap4")


@dataclass
class TablerTheme(Theme):
    """
    Tabler 1.4.0 theme for Flask-Admin.

    Uses Tabler UI (https://tabler.io/) as the front end, loaded via CDN.

    Usage::

        t = TablerTheme()
        admin = Admin(app, name='microblog', theme=t)

    Or with a custom base template::

        t = TablerTheme(base_template='my_base.html')
        admin = Admin(app, name='microblog', theme=t)
    """

    folder: typing.Literal["tabler"] = "tabler"
    base_template: str = "admin/base.html"
