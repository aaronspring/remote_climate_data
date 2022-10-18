import xarray as xr
from matplotlib.colors import ListedColormap

import intake

cat = intake.open_catalog("master.yaml").shapefiles

cmap = ListedColormap(
    [
        "#960000",
        "#FF0000",
        "#FF6E6E",
        "#FFCCCC",
        "#CC8D14",
        "#CCAA54",
        "#FFCC00",
        "#FFFF64",
        "#007800",
        "#005000",
        "#003200",
        "#96FF00",
        "#00D700",
        "#00AA00",
        "#BEBE00",
        "#8C8C00",
        "#5A5A00",
        "#550055",
        "#820082",
        "#C800C8",
        "#FF6EFF",
        "#646464",
        "#8C8C8C",
        "#BEBEBE",
        "#E6E6E6",
        "#6E28B4",
        "#B464FA",
        "#C89BFA",
        "#C8C8FF",
        "#6496FF",
        "#64FFFF",
        "#F5FFFF",
    ]
)


def attach_abbrevs(f):
    """Add abbrevs to GeoDataFrame or xr.DataArray/set."""
    import geopandas as gpd
    import pandas as pd

    table = pd.read_fwf(
        "http://koeppen-geiger.vu-wien.ac.at/data/legend.txt",
        header=None,
        names=["number", "nothing", "abbrev"],
        index=1,
    )
    del table["nothing"]
    table = table.set_index("number")

    if isinstance(f, gpd.geodataframe.GeoDataFrame):
        f = f.merge(table, left_index=True, right_index=True)
    if isinstance(f, (xr.DataArray, xr.Dataset)):
        f.attrs["abbrevs"] = table.abbrev.to_dict()
    else:
        raise NotImplementedError
    return f


def dissolve_to_xrDataArray(gdf, res=1):
    """Dissolve by GRIDCODE and convert with regionmask to res degree grid."""
    gdf = gdf.dissolve("GRIDCODE").drop("ID", axis=1)

    import numpy as np

    assert 180 / res == int(180 / res), "res must divide 180 without remainder"
    grid = xr.DataArray(
        dims=["lat", "lon"],
        coords={
            "lat": np.linspace(-90 + res / 2, 90 - res / 2, int(180 / res)),
            "lon": np.linspace(-180 + res / 2, 180 - res / 2, int(360 / res)),
        },
    )

    import regionmask

    ds = regionmask.mask_geopandas(gdf, grid, wrap_lon=False)
    return ds


def get_all_observed(res=1):
    """Load all observed/historical Geiger Koeppen Classifications as xr.DataArray."""
    obs_periods = ["1901-1925", "1926-1950", "1951-1975", "1976-2000"]

    obs = []
    for p in obs_periods:
        gdf = cat.GeigerKoeppen_shp(period=p).read()
        obs.append(dissolve_to_xrDataArray(gdf, res=res))
    obs = xr.concat(obs, "period")
    obs = obs.assign_coords(period=obs_periods)
    obs.name = "Geiger Koeppen Classification ID"
    obs = attach_abbrevs(obs)
    return obs


def get_all_future(res=1):
    """Load all future scenario Geiger Koeppen Classifications as xr.DataArray."""
    scenarios = ["A1FI", "A2", "B1", "B2"]
    periods = ["2001-2025", "2026-2050", "2051-2075", "2076-2100"]

    fut = []
    for scenario in scenarios:
        scenario_ds = []
        for period in periods:
            scenario_ds.append(
                cat.GeigerKoeppen_xr(
                    transform_kwargs=dict(res=1),
                    target_kwargs=dict(
                        GeigerKoeppen_shp=dict(period=f"{period}_{scenario}")
                    ),
                ).read()
            )
        fut.append(xr.concat(scenario_ds, "period"))
    fut = xr.concat(fut, "scenario").assign_coords(scenario=scenarios, period=periods)
    return fut
