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
    expected = {
        "ocean",
        "land",
        "atmosphere",
        "climate",
        "shapefiles",
        "regionmask",
        "humans",
    }
    actual = set(list(cat))
    assert expected.issubset(actual), f"Missing sub-catalogs: {expected - actual}"


def test_walk_finds_entries(cat):
    """Test that walking the catalog finds dataset entries."""
    entries = list(cat.walk(depth=5))
    assert len(entries) > 0, "Catalog walk returned no entries"


def test_all_entries_have_container(cat):
    """Test that every entry has a container type specified."""
    for name in cat.walk(depth=5):
        entry = cat[name]
        if isinstance(entry, intake.catalog.local.YAMLFileCatalog):  # type: ignore[attr-defined]
            continue
        assert hasattr(entry, "container"), f"Entry {name} has no container"


def test_all_entries_have_description(cat):
    """Test that every entry has a description."""
    for name in cat.walk(depth=5):
        entry = cat[name]
        if isinstance(entry, intake.catalog.local.YAMLFileCatalog):  # type: ignore[attr-defined]
            continue
        assert hasattr(entry, "description"), f"Entry {name} has no description"
