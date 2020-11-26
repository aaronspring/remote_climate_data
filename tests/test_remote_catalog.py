import intake_xarray
import intake
import xarray as xr
from dask.utils import format_bytes
import pytest

intake.config.conf['cache_disabled']=True

cat = intake.open_catalog('https://raw.githubusercontent.com/aaronspring/remote_climate_data/master/master.yaml')

def test_check_all_items():
    for item_str in cat.walk(depth=3):
        print(item_str)
        item = getattr(cat,item_str)
        if isinstance(item, intake_xarray.netcdf.NetCDFSource): # avoid CRU_TS
            ds = item.to_dask()
            assert isinstance(ds, xr.Dataset), print(item_str,'could be accessed by to_dask() but isnt xr.Dataset')
            print('successfully tested',item_str,'\n',type(item),'\n',ds.dims, '\n',ds.coords, '\nsize = ',format_bytes(ds.nbytes),'\n')
        elif isinstance(item, (intake_geopandas.RegionmaskSource, intake_geopandas.ShapefileSource)):
            region = item.read()
            print('successfully tested',item_str,'\n',type(item))
        else:
            print('couldnt test',item_str,'\n',type(item),'\n',item,'\n')
    import os
    #assert not os.path.exists('HadCRUT4'), print('files got cached',os.listdir())
