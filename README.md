# flask-admin-tabler

A [Tabler UI](https://tabler.io/) theme for [Flask-Admin](https://github.com/pallets-eco/flask-admin).

## Installation

```shell
pip install flask-admin-tabler
```

## Quick start

Call `theme.init_app(app)` **before** creating the `Admin` instance so that the
Tabler templates are registered with higher priority than Flask-Admin's default
Bootstrap ones.

```python
from flask import Flask
from flask_admin import Admin
from flask_admin_tabler import TablerTheme

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"

theme = TablerTheme()
theme.init_app(app)          # must come before Admin(app, ...)

admin = Admin(app, name="My App", theme=theme)
```

Navigate to `/admin/` and you'll see the Tabler UI instead of the default
Bootswatch theme.

A fully runnable example (including a SQLAlchemy model and sample data) is
available in [`examples/quickstart.py`](examples/quickstart.py):

```shell
pip install flask-admin-tabler flask-sqlalchemy
python examples/quickstart.py
# open http://127.0.0.1:5000/admin/
```

---

## Configuration reference

All options are passed to `TablerTheme(...)` as keyword arguments.

### `layout`

Controls the navigation structure.

| Value | Description |
|-------|-------------|
| `"horizontal"` | **(default)** Sticky top navbar |
| `"vertical"` | Left sidebar |

```python
theme = TablerTheme(layout="vertical")
```

See [`examples/sidebar_dark.py`](examples/sidebar_dark.py) for a full example.

---

### `color_scheme`

Light or dark mode.  Sets `data-bs-theme` on the `<html>` element.

| Value | Description |
|-------|-------------|
| `"light"` | **(default)** Light mode |
| `"dark"` | Dark mode |

```python
theme = TablerTheme(color_scheme="dark")
```

---

### `primary_color`

Accent color used throughout the UI (buttons, active links, badges …).
Sets `data-bs-theme-primary` on the `<html>` element.
Default is `None` (Tabler's built-in blue).

Allowed values: `"blue"`, `"azure"`, `"indigo"`, `"purple"`, `"pink"`,
`"red"`, `"orange"`, `"yellow"`, `"lime"`, `"green"`, `"teal"`, `"cyan"`.

```python
theme = TablerTheme(primary_color="teal")
```

---

### `font`

Font family applied globally.
Sets `data-bs-theme-font` on the `<html>` element.
Default is `None` (Tabler's built-in sans-serif).

Allowed values: `"sans-serif"`, `"serif"`, `"monospace"`, `"comic"`.

```python
theme = TablerTheme(font="serif")
```

---

### `base_color`

Gray shade used for backgrounds, borders, and muted text.
Sets `data-bs-theme-base` on the `<html>` element.
Default is `None` (Tabler's built-in gray).

Allowed values: `"slate"`, `"gray"`, `"zinc"`, `"neutral"`, `"stone"`.

```python
theme = TablerTheme(base_color="zinc")
```

---

### `corner_radius`

Border-radius scale factor that controls how rounded UI elements appear.
Sets `data-bs-theme-radius` on the `<html>` element.
Default is `None` (Tabler's built-in value of `1`).

Allowed values: `"0"`, `"0.5"`, `"1"`, `"1.5"`, `"2"`.

```python
theme = TablerTheme(corner_radius="1.5")
```

---

### `tabler_icons`

Whether to load the [Tabler Icons](https://tabler.io/icons) webfont from CDN.

| Value | Description |
|-------|-------------|
| `True` | **(default)** Load icons CSS from jsDelivr CDN |
| `False` | Skip loading the icons CSS |

```python
theme = TablerTheme(tabler_icons=False)
```

When icons are loaded you can use them in menu items via `icon_type="tabler"`:

```python
from flask_admin.menu import MenuView

admin.add_view(MenuView("Dashboard", "/admin/", icon_type="tabler", icon_value="home"))
```

This renders `<i class="ti ti-home"></i>` in the navigation.

---

## All options together

```python
from flask import Flask
from flask_admin import Admin
from flask_admin_tabler import TablerTheme

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"

theme = TablerTheme(
    layout="vertical",       # sidebar navigation
    color_scheme="dark",     # dark mode
    primary_color="teal",    # teal accent
    font="sans-serif",       # sans-serif font
    base_color="gray",       # gray base
    corner_radius="1.5",     # rounded corners
)
theme.init_app(app)

admin = Admin(app, name="My App", theme=theme)
```

The settings are applied server-side as `data-bs-*` HTML attributes — no
JavaScript or localStorage involved:

```html
<html lang="en"
  data-bs-theme="dark"
  data-bs-theme-primary="teal"
  data-bs-theme-font="sans-serif"
  data-bs-theme-base="gray"
  data-bs-theme-radius="1.5"
>
```

See [`examples/theme_settings.py`](examples/theme_settings.py) for a full
runnable example.

---

## How it works

`TablerTheme.init_app(app)` registers a Flask blueprint named
`flask_admin_tabler` that:

1. **Templates** — exposes `flask_admin_tabler/templates/tabler/` as a template
   folder.  Because this blueprint is registered *before* Flask-Admin's admin
   blueprint, Flask resolves `admin/base.html` (and all other admin templates)
   from here first.
2. **Static files** — serves the small amount of theme-specific CSS (e.g.
   `admin/css/tabler/admin.css`) at `/static/flask_admin_tabler/`.

Tabler's core CSS and JS are loaded from the jsDelivr CDN — no local copies
needed.

---

## Requirements

- Python ≥ 3.10
- flask-admin ≥ 2.0.2
