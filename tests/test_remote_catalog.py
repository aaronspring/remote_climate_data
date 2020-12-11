import intake_xarray
import intake_geopandas
import intake
import xarray as xr
from dask.utils import format_bytes
import pytest

# dont test the online catalog but current branch
cat = intake.open_catalog('master.yaml')

def test_check_all_items():
    """Test all items.to_dask() except ceda requiring credentials"""
    for item_str in cat.walk(depth=3):
        print(item_str)
        if 'CRU_TS' not in item_str: # avoids also CRU datasets requiring credentials at ceda
            item = getattr(cat, item_str)
            if isinstance(item, intake_xarray.netcdf.NetCDFSource) and item_str not in ['ocean.SOM_FFN', 'ocean.CSIR-ML6']:  # avoids too large (>500MB) datasets
                ds = item.to_dask()
                assert isinstance(ds, xr.Dataset), print(item_str, 'could be accessed by to_dask() but isnt xr.Dataset')
                print('successfully tested', item_str, '\n',type(item), '\n', ds.dims, '\n', ds.coords, '\nsize = ', format_bytes(ds.nbytes), '\n')
            elif isinstance(item, (intake_geopandas.RegionmaskSource, intake_geopandas.ShapefileSource)):
                region = item.read()
                print('successfully tested', item_str, '\n', type(item))
            elif isinstance(item, intake_excel.ExcelSource):
                df = item.read()
                print('successfully tested', item_str, '\n', type(df),'\n', df.head())
            else:
                print('couldnt test', item_str, '\n', type(item), '\n', item, '\n')
