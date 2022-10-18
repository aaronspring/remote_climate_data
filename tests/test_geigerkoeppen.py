import xarray as xr
import pytest

from remote_climate_data.utils.geigerkoeppen import get_all_observed, get_all_future

@pytest.mark.parametrize("get", [get_all_observed, get_all_future])
def test_get_all(get):
    """Test get_all_* returns xr.DataArray."""
    assert isinstance(get(), xr.DataArray)
