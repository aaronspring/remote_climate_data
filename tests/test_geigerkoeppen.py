import pytest
import xarray as xr

from remote_climate_data.utils.geigerkoeppen import get_all_future, get_all_observed


@pytest.mark.parametrize("get", [get_all_observed, get_all_future])
def test_get_all(get):
    """Test get_all_* returns xr.DataArray."""
    assert isinstance(get(), xr.DataArray)
