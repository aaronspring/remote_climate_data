# AGENTS.md

## Project Overview

`remote_climate_data` is a collection of remote climate datasets accessed via [intake](https://intake.readthedocs.io/) catalogs with disk caching via `fsspec`. It provides YAML-based intake catalogs for ocean, land, atmosphere, climate, shapefiles, regionmask, and human geoinformation data.

## Repository Structure

- `master.yaml` — Top-level intake catalog referencing sub-catalogs in `catalogs/`
- `catalogs/` — YAML intake catalog files (`ocean.yaml`, `atmosphere.yaml`, `land.yaml`, `climate.yaml`, `shapefiles.yaml`, `regionmask.yaml`, `humans.yaml`) and sub-catalog directories
- `remote_climate_data/` — Python package (minimal, mainly `__init__.py` and `utils/`)
- `tests/` — pytest tests (`test_*.py`)
- `notebooks/` — Jupyter notebooks (e.g., `demo.ipynb`)

## Code Style & Conventions

- **Python**: Ruff (line-length 88, replaces black/flake8/isort)
- **YAML**: yamllint with max line-length 88
- **Type checking**: ty (run `ty check` or `uvx ty check`)
- Prek hooks enforce all of the above — run `prek run --all-files` to check
- Tests use `pytest` (config in `setup.cfg`, test files in `tests/`)

## Working with Catalogs

- Catalog files are YAML following the [intake](https://intake.readthedocs.io/) v1 catalog spec
- Pinned to `intake<2` (intake v2 "Take2" breaks YAML catalog format and plugins)
- Use `"simplecache::"` prefix in `urlpath` to enable caching
- Include `metadata` with documentation URLs and DOIs
- Use `parameters` for templating versions/variables in `urlpath`
- New datasets go into the appropriate sub-catalog: `ocean`, `land`, `atmosphere`, or `climate`
- New shapefiles go into `shapefiles.yaml`

## Testing

```bash
pytest --durations=20
```

- `test_remote_catalog.py` — Structural tests (catalog loads, entries have drivers/URLs)
- `test_url_availability.py` — Network tests checking all dataset URLs return HTTP 200
- `test_caching.py` — Smoke tests for fsspec caching

CI runs on GitHub Actions (`testing.yml`) using conda with `environment.yml` on ubuntu-latest with Python 3.12.

## Dependencies

Managed via `uv` (or `environment.yml` for conda). Build config in `pyproject.toml` (PEP 621, setuptools backend). Key libraries: `intake<2`, `intake-xarray`, `fsspec`, `xarray`, `netcdf4`, `regionmask`, `hvplot`.

To install dependencies with uv:
```bash
uv sync
# or for optional dependencies:
uv sync --all-extras
```

## Binder

Binder uses a separate minimal environment at `binder/environment.yml` to keep builds fast and reliable.
