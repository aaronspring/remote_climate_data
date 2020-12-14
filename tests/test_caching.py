import sys
sys.path.append('utils')
import pytest
import intake
import shutil
import os

from caching import cache_all_catalog_items

@pytest.fixture()
def cat():
    return intake.open_catalog('master.yaml')

def test_cache_all_catalog_items(cat):
    folder = 'test_cache'
    cache_all_catalog_items(cat.climate,folder)
    assert 'nina34.data' in os.listdir(folder)
    shutil.rmtree(folder)
