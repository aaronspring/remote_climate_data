import intake
import intake_excel
import intake_geopandas
import intake_xarray
import pytest
import xarray as xr
from dask.utils import format_bytes


# dont test the online catalog but current branch
@pytest.fixture
def cat():
    return intake.open_catalog("master.yaml")


def test_check_all_items(cat):
    """Test all items.to_dask() except ceda requiring credentials"""
    for item_str in cat.walk(depth=3):
        print(item_str)
        if "CRU_TS" in item_str:
            print("avoid testing CRU_TS requiring credentials at ceda\n")
        else:
            item = getattr(cat, item_str)
            if isinstance(
                item, (intake_xarray.NetCDFSource, intake_xarray.OpenDapSource)
            ) and item_str not in [
                "ocean.SOM_FFN",
                "ocean.CSIR-ML6",
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
                    f"size = {len(region.names)}."
                )
            elif isinstance(
                item, (intake.source.csv.CSVSource, intake_excel.ExcelSource)
            ):
                df = item.read()
                print(f"successfully tested {item_str} type = {type(df)}\n {df.head()}")
            else:
                print(f"couldnt test {item_str} type = {type(item)} {item}\n")
