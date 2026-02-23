[![testing](https://github.com/aaronspring/remote_climate_data/actions/workflows/testing.yml/badge.svg)](https://github.com/aaronspring/remote_climate_data/actions/workflows/testing.yml) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aaronspring/remote_climate_data/master?urlpath=lab%2Ftree%2Fnotebooks%2Fdemo.ipynb)

# remote_climate_data
a collection of remote climate data accessed via `intake` cached to disk

## Install
```bash
uv sync
# or with optional dependencies:
uv sync --all-extras
```

## Run commands with uv
```bash
uv run pytest  # run tests
uv run prek run --all-files  # run pre-commit hooks on all files
uv run ty check  # run type checking
```

## Catalog

<details>
<summary>Show catalog entries</summary>

```
ocean:
  - carbon (subcatalog)
  - HadSST3
  - HadSST4
  - HadISST1
  - WOA2018
  - OISSTv21
  - OISSTv2
  - OISSTv2_thredds

land:
  - CRUTEM4
  - CRUTEM4v
  - CRUTEM5
  - CRUTEM5alt
  - Leaf_Area_Index

atmosphere:
  - HadCRUT4
  - HadCRUT5
  - HadCRUT5_Non-Infilled
  - CRU_TS (subcatalog)
  - GISTEMP
  - NOAA_GlobalTemp
  - BerkeleyEarth_land
  - BerkeleyEarth_land_and_ocean
  - Cowtan_and_Way_Long
  - trace_gases_at_stations
  - NCEP_6h
  - NCEP_6h_gauss
  - NCEP_monthly
  - NCEP_monthly_gauss
  - fossil_fuel_emissions_gridded
  - NOAA_carbon_tracker
  - xco2_v4
  - pr_GPCP
  - pr_TRMM

climate:
  - NOAA_correlation
  - NOAA_correlation_xr
  - Global_Carbon_Budget_2025
  - Global_Carbon_Budget_2021

shapefiles:
  - Countries
  - IPCCAR6
  - geometric_features
  - GeigerKoeppen_shp
  - GeigerKoeppen_xr

regionmask:
  - Countries
  - IPCCAR6
  - MEOW
  - FEOW
  - TEOW

humans:
  - GHS
```

</details>

**YAML files:** [master.yaml](master.yaml) · [atmosphere.yaml](catalogs/atmosphere.yaml) · [climate.yaml](catalogs/climate.yaml) · [humans.yaml](catalogs/humans.yaml) · [land.yaml](catalogs/land.yaml) · [ocean.yaml](catalogs/ocean.yaml) · [regionmask.yaml](catalogs/regionmask.yaml) · [shapefiles.yaml](catalogs/shapefiles.yaml)

## Usage
```python
import intake
cat = intake.open_catalog('https://raw.githubusercontent.com/aaronspring/remote_climate_data/master/master.yaml')
cat.atmosphere.HadCRUT5.to_dask()
```
```
<xarray.Dataset> Size: 42MB
Dimensions:           (time: 2028, latitude: 36, longitude: 72, bnds: 2)
...
```

```python
import hvplot.pandas
gcb = cat.climate().Global_Carbon_Budget_2025.read()
gcb.hvplot(y=['fossil emissions excluding carbonation', 'land-use change emissions',
               'atmospheric growth', 'ocean sink', 'land sink'],
           title='Global Carbon Budget 2025')
```
```
      fossil emissions excluding carbonation  ...  budget imbalance
Year                                          
1959                                2.416788  ...          1.168380
...
2024                               10.534546  ...         -1.691863

[66 rows x 7 columns]
```

Explore the whole catalog:
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
- [`intake_excel`](https://github.com/edjdavid/intake-excel) for Excel `xls` and `xlsx` [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/climate.yaml#L35)] (see [`excel_source.py`](remote_climate_data/excel_source.py) for custom driver if package unavailable)
- [`intake_geopandas`](https://github.com/intake/intake_geopandas) for shapefiles `shp` [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/shapefiles.yaml#L11)], GeoJSON `geo.json` [[example](https://github.com/aaronspring/remote_climate_data/blob/1209c5ebf5877b09b4403ea60da6d97b374b7b5c/catalogs/shapefiles.yaml#L57)], GeoParquet `parquet`, `PostGIS` databases, `Spatialite` databases
- [`regionmask`](https://regionmask.readthedocs.io/) for aggregating over geoshapes

## Similar projects
- Pangeo's cloud data catalogs for multi GB and TB datasets: https://github.com/pangeo-data/pangeo-datastore
