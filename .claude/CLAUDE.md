# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A German desktop GUI (tkinter) used by volunteer firefighters ("Freiwillige Feuerwehr") to track personal protective equipment (PSA = Persönliche Schutzausrüstung), special PSA (Wathosen, Schnittschutzhose, …), members, and equipment checks. The app generates printable Word documents from `.docx` templates by replacing tokens with database values. Ships as a single PyInstaller binary. UI labels and many domain terms are German — keep them German.

## Commands

Uses `uv` for dependency management. Targets Python 3.12 (per `.python-version`); `pyproject.toml` requires `>=3.11`.

| Task | Command |
| --- | --- |
| Install deps | `make install` (`uv sync`) |
| Run the app from source | `make run` (`PYTHONPATH=./ uv run ./src/main.py`) |
| Build the standalone binary | `make exe` (writes to `dist/`) |
| Format + lint | `make lint` (black → isort → ruff check) |
| Install git hooks | `make hooks` (`pre-commit install`; requires `brew install pre-commit`) |
| Clean build artifacts | `make clean` |

No test suite exists in this repo. Don't fabricate a `pytest` step when verifying changes — run the app via `make run` or build via `make exe` instead.

**Lint caveat:** `.pre-commit-config.yaml` pins Black `24.10.0` on `python3.13`, while `pyproject.toml` dev-deps Black `>=25.1.0` and `.python-version` is `3.12`. `make lint` and the pre-commit hook can produce different formatting. If a diff churns in CI, check which Black ran.

## Architecture

### Entry point and frame swapping

`src/main.py` defines `App(tkinter.Tk)`. It builds a menubar and swaps `ViewProtocol` frames in/out via `App.show_frame(page_name)`, destroying the previous frame. The registry is `App.frames: dict[str, Type[ViewProtocol-subclass]]`. `EquipmentGUI` is registered and menu-wired but currently commented out — re-enable both `App.frames` and the `equipment_menu` block together if reviving it.

### Views (`src/views/`)

Every view subclasses `ViewProtocol(tkinter.Frame)` and follows this layout:

1. `CustomTreeView` (`src/views/customtreeview.py`) at the top — wraps `ttk.Treeview`, exposes `ensure_one_selected()` returning `(selection, item)` or `None` (used with `:=` walrus).
2. Bottom row of `tkinter.LabelFrame`s for Add / Bearbeiten (edit) / Drucken (print).
3. Buttons created via `button_pack` / `button_grid` / `entry_with_label` helpers in `src/views/uielements.py`.

Each view loads its own data from `db.session` directly in `__init__` (e.g. `init_data`, `init_treeview_data`, `initData` — naming is inconsistent across views).

### Database (`src/models/`)

SQLAlchemy 2.x with SQLite. **The `__init__.py` order is intentional and must be preserved:**

```python
BASE = declarative_base()
from .equipment import Equipment  # noqa: E402, F401
# ... other models, all with the same noqa pair
ENGINE = sqlalchemy.create_engine(_DB_URI)
BASE.metadata.create_all(ENGINE)
session = DBSession()
```

A **single module-level `session`** is shared across the app. Views do `import src.models as db` and then `db.session.add(...)` / `db.session.commit()` directly. There is no repository layer or unit-of-work pattern.

**Soft-delete convention:** every model has `deleted: Boolean`, `dateCreated: Date`, `dateEdited: Date`. Reads filter `.deleted.is_(False)`. Deletes set `deleted=True` + bump `dateEdited`; they do not issue `DELETE`. Follow this when adding new models or queries.

Tables: `Member`, `Psa` (1:1 with Member via `mid`), `SpecialPsa` (FK to `SpecialPsaTemplates.type`), `SpecialPsaTemplates`, `Equipment`, `EquipmentChecks` (FK to `Equipment.id`). `Member.get_by_id` / `get_all` and `Equipment.get_by_id` / `get_all` are the only model-level query helpers — most queries are inlined in views with `select(...)`.

### Path resolution (`src/logic/pathes.py`)

Resolves the data directory differently depending on whether the app is running from source or as a PyInstaller-frozen binary:

- **Frozen** (`sys.frozen` is true): data lives at `data/` next to the executable.
- **From source**: data lives at `../data` relative to `src/logic/`, i.e. `src/data/`.

This module defines `main_path`, `report_path`, `out_path` (always `<reports>/out.docx`), `logs_path`, `log_path`. The SQLite DB URL in `src/models/__init__.py` and template paths in `src/template_processing/*.py` both build off `main_path` — any code touching files on disk should go through these constants, not hard-code paths.

Bundled assets (`.docx` templates) live at `src/data/templates/*.docx` in dev. The PyInstaller build copies `data/` next to the exe at install time.

### Template / document pipeline (`src/template_processing/`)

Each "Drucken" button in a view:

1. Builds a flat `parameters: dict[str, str]` of token → replacement (keys like `lastname`, `numej`, `yhelm`, …).
2. Calls into `src.template_processing.compose_*` (`compose_specificpsa_for_member`, `compose_wholepsa`, `compose_specificpsa_with_path`, `compose_multiple_equipment`).
3. The composer opens the matching `template_*.docx` via `python-docx`, walks all tables → rows → cells → paragraphs, runs a regex `paragraph_replace_text` (run-aware so formatting survives), stitches multiple docs with `docxcompose.Composer`, and writes to `out_path`.
4. The view then calls `open_file(out_path)` (`src/logic/files.py`, dispatches to `open` on macOS / `os.startfile` on Windows — **Linux is not handled**).

`paragraph_replace_text` is a vendored upstream snippet (`src/template_processing/paragraph_replace_text.py`); changing it risks breaking templates whose tokens straddle multiple `run`s.

The `"BaseEquipment"` template (`template_equipment.docx`) is paginated nine checks per page; see `compose_single_equipment` in `compose_equipment.py` for the pagination math.

### Initial data

`src/logic/initialize_database.py::add_special_psa()` seeds `SpecialPsaTemplates` rows. It is wired to the "Über → Initialisieren Spezieller PSA Vorlagen" menu item and is **not idempotent** — calling it twice inserts duplicates. Add an existence check before reusing this pattern.

### Logging

`src/logic/logger.py` configures a module-level `logger` with a `TimedRotatingFileHandler` (midnight rotation, suffix `%Y-%m-%d`) writing to `log_path`, plus a console handler. Import as `from src.logic.logger import logger`. `App.report_callback_exception` is wired to log uncaught tkinter callback exceptions.

## Style and formatting

`black` line length 120, `isort` profile `black`, `ruff` line length 120 (see `pyproject.toml`). German identifiers and German UI strings are expected — don't translate them.
