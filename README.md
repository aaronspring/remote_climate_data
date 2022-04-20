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
- [`intake`](https://intake.readthedocs.io/en/latest/) for catalogs and `csv` and [`zarr`](https://github.com/zarr-developers/zarr-python)
- [`fsspec`](https://filesystem-spec.readthedocs.io/en/latest/features.html#url-chaining) for caching
- [`intake_xarray`](https://intake-xarray.readthedocs.io/en/latest/) for:
  - `nc` using [`netcdf4`](https://github.com/Unidata/netcdf4-python) [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/atmosphere.yaml#L64)]
  - `tif` using [`rioxarray`](https://github.com/corteva/rioxarray) [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/humans.yaml#L42)]
  - `grib` using [`cfgrib`](https://github.com/ecmwf/cfgrib/) [[example missing]()]
- [`intake_thredds`](https://github.com/intake/intake-thredds) for using [`intake_xarray`](https://intake-xarray.readthedocs.io/en/latest/) via [THREDDS](https://www.unidata.ucar.edu/software/tds/current/) [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/atmosphere.yaml#L322)]
- [`intake_excel`](https://github.com/edjdavid/intake-excel) for Excel `xls` and `xlsx` [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/climate.yaml#L35)]
- [`intake_geopandas`](https://github.com/intake/intake_geopandas) for shapefiles `shp` [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/shapefiles.yaml#L11)], GeoJSON `geo.json` [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/shapefiles.yaml#L57)], GeoParquet `parquet`, `PostGIS` databases, `Spatialite` databases
- [`regionmask`](https://regionmask.readthedocs.io/) for aggregating over geoshapes
- [`hvplot`](https://hvplot.holoviz.org/index.html) for plotting [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/atmosphere.yaml#L48)]

## Similar projects
- Pangeo's cloud data catalogs for multi GB and TB datasets: https://github.com/pangeo-data/pangeo-datastore
