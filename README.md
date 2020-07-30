# remote_climate_data
a collection of remote climate data accessed via `intake` cached to disk


## Usage
```python
import intake
cat = intake.open_catalog('https://raw.githubusercontent.com/aaronspring/remote_climate_data/master/master.yaml')
cat.atmosphere.HadCRUT4.to_dask()
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
- PRs for new remote climate datasets are very welcome
- shapefiles via `intake_geopandas` once https://github.com/intake/intake_geopandas/pull/17 is merged
- Extendable with THREDDS catalogs via https://github.com/NCAR/intake-thredds once https://github.com/NCAR/intake-thredds/pull/3 is merged


## Relies on
- `intake`: https://intake.readthedocs.io/en/latest/
- `intake_xarray`: https://intake-xarray.readthedocs.io/en/latest/
- `intake_geopandas`: https://github.com/aaronspring/intake_geopandas.git@AS_cache
- (optional) `hvplot`: https://hvplot.holoviz.org/index.html for plotting


## Similar projects
- Pangeo's cloud data catalogs: https://github.com/pangeo-data/pangeo-datastore
- what https://github.com/intake/intake-datasets intends to be
