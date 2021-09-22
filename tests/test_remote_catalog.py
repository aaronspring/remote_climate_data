import intake
import intake_excel
import intake_geopandas
import intake_thredds
import intake_xarray
import pytest
import xarray as xr
from dask.utils import format_bytes


@pytest.fixture
def cat():
    """don't test the online master catalog but current branch"""
    return intake.open_catalog("master.yaml")


# don't test the online catalog but current branch
cat2 = intake.open_catalog("master.yaml")
item_strs = [
    i
    for i in cat2.walk(depth=3)
    if not isinstance(cat2[i], intake.catalog.local.YAMLFileCatalog)
]


@pytest.mark.parametrize("item_str", item_strs)
def test_plots(cat, item_str):
    """Test all items.plot.my_plot()"""
    item = getattr(cat, item_str)
    plots = item.plots
    if len(plots) > 0:
        for plot in plots:
            print("test", item_str, plot)
            getattr(item.plot, plot)()


@pytest.mark.parametrize("item_str", item_strs)
def test_item(cat, item_str):
    """Test all items.to_dask() except ceda requiring credentials and too large files"""
    if "CRU_TS" in item_str:
        print("avoid testing CRU_TS requiring credentials at ceda\n")
    else:
        item = getattr(cat, item_str)
        if "ftp" in item.urlpath:
            print("{item} found source from ftp, skip testing")
            return 0
        if isinstance(item, (intake_xarray.NetCDFSource, intake_xarray.OpenDapSource)):
            # don't cache
            urlpath = item.urlpath.replace("simplecache::", "")
            try:
                ds = item(urlpath=urlpath).to_dask()
            except:
                ds = item.to_dask()
            assert isinstance(ds, xr.Dataset)
            print(
                f"successfully tested {item_str} type = {type(item)}\n {ds.dims}"
                f"{ds.coords} size = {format_bytes(ds.nbytes)}\n"
            )
        elif isinstance(
            item,
            (intake_geopandas.RegionmaskSource, intake_geopandas.ShapefileSource),
        ):
            region = item.read()
            print(
                f"successfully tested {item_str}: type = {type(item)}, "
                f"size = {len(region)}."
            )
        elif isinstance(item, intake_thredds.source.THREDDSMergedSource):
            # don't cache
            urlpath = item.urlpath.replace("simplecache::", "")  # ?
            if "IOSST" in item_str:
                ds = item(year="???0").to_dask()
                assert isinstance(ds, xr.Dataset)
                print(f"successfully tested {item_str}")
            if "NCEP" in item_str:
                ds = item(year="19?0").to_dask()
                assert isinstance(ds, xr.Dataset)
                print(f"successfully tested {item_str}")
        elif isinstance(item, (intake.source.csv.CSVSource, intake_excel.ExcelSource)):
            df = item.read()
            print(f"successfully tested {item_str} type = {type(df)}\n {df.head()}")
        else:
            print(f"couldnt test {item_str} type = {type(item)} {item}\n")
