import os

import fsspec
import intake
import pytest


@pytest.fixture()
def cat():
    return intake.open_catalog("master.yaml")


folder = "test_cache"
fsspec.config.conf["simplecache"] = {
    "cache_storage": folder,
    "same_names": True,
}


def test_cache_all_catalog_items_csv(cat):
    """Test that files are downloaded."""
    cat.climate.NOAA_correlation.to_dask()
    assert "nina34.data" in os.listdir(folder)


def test_cache_all_catalog_items_nc(cat):
    """Test that files are downloaded."""
    cat.atmosphere.HadCRUT4.to_dask()
    assert "HadCRUT.4.6.0.0.median.nc" in os.listdir(folder)
