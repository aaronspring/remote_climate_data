import os
import shutil
import sys

import intake
import pytest

sys.path.append("utils")
from caching import cache_all_catalog_items


@pytest.fixture()
def cat():
    return intake.open_catalog("master.yaml")


def test_cache_all_catalog_items_csv(cat):
    """Test that files are downloaded."""
    folder = "test_cache"
    cache_all_catalog_items(cat.climate, folder)
    assert "nina34.data" in os.listdir(folder)
    shutil.rmtree(folder)


def test_cache_all_catalog_items_nc(cat):
    """Test that files are downloaded."""
    folder = "test_cache"
    cache_all_catalog_items(cat.atmosphere, folder)
    assert "HadCRUT.4.6.0.0.median.nc" in os.listdir(folder)
    # shutil.rmtree(folder)
