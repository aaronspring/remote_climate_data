"""Test that catalogs load and enumerate correctly (no network downloads)."""

import intake
import pytest


@pytest.fixture(scope="module")
def cat():
    """Load the local master catalog (current branch, not online)."""
    return intake.open_catalog("master.yaml")


def test_catalog_loads(cat):
    """Test that the master catalog loads without error."""
    assert cat is not None


def test_catalog_has_subcatalogs(cat):
    """Test that expected sub-catalogs exist."""
    expected = {"ocean", "land", "atmosphere", "climate", "shapefiles", "regionmask", "humans"}
    actual = set(list(cat))
    assert expected.issubset(actual), f"Missing sub-catalogs: {expected - actual}"


def test_walk_finds_entries(cat):
    """Test that walking the catalog finds dataset entries."""
    entries = list(cat.walk(depth=5))
    assert len(entries) > 0, "Catalog walk returned no entries"


def test_all_entries_have_driver(cat):
    """Test that every entry has a driver specified."""
    for name in cat.walk(depth=5):
        entry = cat[name]
        if isinstance(entry, intake.catalog.local.YAMLFileCatalog):
            continue
        assert hasattr(entry, "container") or hasattr(entry, "driver"), (
            f"Entry {name} has no driver"
        )


def test_all_entries_have_urlpath_or_path(cat):
    """Test that every non-derived, non-catalog entry has urlpath or path."""
    for name in cat.walk(depth=5):
        entry = cat[name]
        if isinstance(entry, intake.catalog.local.YAMLFileCatalog):
            continue
        if isinstance(entry, intake.source.derived.GenericTransform):
            continue
        has_url = hasattr(entry, "urlpath") and entry.urlpath
        has_path = hasattr(entry, "path") and entry.path
        assert has_url or has_path, f"Entry {name} has no urlpath or path"
