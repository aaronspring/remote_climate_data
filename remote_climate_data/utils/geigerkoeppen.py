import xarray as xr

def attach_abbrevs(f):
    import geopandas as gpd
    table = pd.read_fwf("http://koeppen-geiger.vu-wien.ac.at/data/legend.txt", header=None, names=["number","nothing","abbrev"], index=1)
    del table["nothing"]
    table = table.set_index("number")
    
    if isinstance(f, gpd.geodataframe.GeoDataFrame):
        f = f.merge(table, left_index=True, right_index=True)
    if isinstance(f, [xr.DataArray, xr.Dataset]):
        f.attrs["abbrevs"] = table.abbrev
    else:
        raise NotImplementedError
    return f

def dissolve_to_xrDataArray(gdf, res=1):
    gdf = gdf.dissolve("GRIDCODE").drop("ID", axis=1)
    
    import numpy as np
    
    assert 180/res == 180//res, "res must divide 180 without remainder"
    grid = xr.DataArray(dims=["lat","lon"],coords={
        'lat': np.linspace(-90+res/2, 90-res/2, 180//res),
        'lon': np.linspace(-180+res/2, 180-res/2, 360//res)
    })
    
    import regionmask
    
    ds = regionmask.mask_geopandas(gdf, grid)
    return ds

def get_all_observed(res=1):
    obs_periods = ['1901-1925', '1926-1950', '1951-1975', '1976-2000']

    import intake
    cat = intake.open_catalog("master.yaml").shapefiles
    obs = []
    for p in obs_periods:
        gdf = cat.GeigerKoeppen_shp(period=p).read()
        obs.append(dissolve_to_xrDataArray(gdf, res=res))
    obs = xr.concat(obs,"period")
    obs = obs.assign_coords(period=obs_periods)
    obs.name = "Geiger Koeppen Classification ID"
    obs = attach_abbrevs(obs)
    return obs