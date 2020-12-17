import intake
import intake_excel
import intake_geopandas
import intake_thredds
import intake_xarray
import pytest
import xarray as xr
from dask.utils import format_bytes


# don't test the online catalog but current branch
@pytest.fixture
def cat():
    return intake.open_catalog("master.yaml")


cat2 = intake.open_catalog("master.yaml")
item_strs = [
    i
    for i in cat2.walk(depth=3)
    if not isinstance(cat2[i], intake.catalog.local.YAMLFileCatalog)
]


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
        if isinstance(
            item, (intake_xarray.NetCDFSource, intake_xarray.OpenDapSource)
        ) and item_str not in [
            "ocean.carbon.MPI-SOM_FFN",
            "ocean.carbon.CSIR-ML6",
        ]:  # avoids too large (>500MB) datasets
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
            if "IOSST" in item_str:
                ds = item(year="???0").to_dask()
                print(f"successfully tested {item_str}")
        elif isinstance(item, (intake.source.csv.CSVSource, intake_excel.ExcelSource)):
            df = item.read()
            print(f"successfully tested {item_str} type = {type(df)}\n {df.head()}")
        else:
            print(f"couldnt test {item_str} type = {type(item)} {item}\n")
