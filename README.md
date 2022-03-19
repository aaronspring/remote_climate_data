[![testing](https://github.com/aaronspring/remote_climate_data/actions/workflows/testing.yml/badge.svg)](https://github.com/aaronspring/remote_climate_data/actions/workflows/testing.yml) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aaronspring/remote_climate_data/master?urlpath=lab%2Ftree%2Fnotebooks%2Fdemo.ipynb) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/aaronspring/remote_climate_data/master.svg)](https://results.pre-commit.ci/latest/github/aaronspring/remote_climate_data/master)

# remote_climate_data
a collection of remote climate data accessed via `intake` cached to disk

## Usage
```python
import intake
cat = intake.open_catalog('https://raw.githubusercontent.com/aaronspring/remote_climate_data/master/master.yaml')
cat.atmosphere.HadCRUT5.to_dask()
```

To explore the whole catalog, you can try:
```python
cat.walk()
```


## Goal
Make data access for climate data easy:
- cacheable data
- documentation attached in metadata
- shareable catalogs
- quick vizualisations


## Contribute and extend
- PRs for new remote climate datasets or useful geoshapes are very welcome


## Relies on
- `intake`: https://intake.readthedocs.io/en/latest/ for catalogs and `csv`
- `intake_xarray`: https://intake-xarray.readthedocs.io/en/latest/ for NetCDF `nc`
- `intake_thredds`: https://github.com/intake/intake-thredds for NetCDF `nc` via THREDDS
- tif opt
- cfgrib opt via intake xarray
- `intake_excel`: https://github.com/edjdavid/intake-excel/issues for Excel `xls` and `xlsx`
- `intake_geopandas`: https://github.com/intake_geopandas/intake_geopandas.git for shapefiles `shp`, GeoJSON `geo.json`, GeoParquet `parquet`, `PostGIS` databases, `Spatialite` databases
- `regionmask`: https://regionmask.readthedocs.io/ for aggregating over geoshapes
- `hvplot`: https://hvplot.holoviz.org/index.html for plotting


## Similar projects
- Pangeo's cloud data catalogs: https://github.com/pangeo-data/pangeo-datastore
- what https://github.com/intake/intake-datasets intends to be
