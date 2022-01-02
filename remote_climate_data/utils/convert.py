import pandas as pd
import xarray as xr


def monthly_csv_to_DataArray(df, freq="MS"):
    """Convert dataframes from NOAA catalog items to xr.DataArray.

    Example:
        >>> cat = intake.open_catalog('master.yaml')
        >>> df = cat.climate.NOAA_correlation.read()
        >>> da = monthly_csv_to_DataArray(df)
        >>> da
        <xr.DataArray> ...
    """
    df = df.set_index("year")
    df = df.apply(pd.to_numeric, errors="coerce")
    initial = df.first_valid_index()
    if len(str(initial)) >= 4:
        initial = str(initial)[:4]
    initial = int(initial)
    return xr.DataArray(
        df.values.flatten(),
        dims="time",
        coords={
            "time": xr.cftime_range(str(initial), freq=freq, periods=df.values.size)
        },
    )


def molC_per_yr_to_kg_per_s(ds, **kwargs):
    """Convert xr objects from molC/year to kg/seconds."""
    assert isinstance(ds, (xr.DataArray, xr.Dataset))
    variables = list(ds.data_vars if isinstance(ds, xr.Dataset) else ds.name)
    for v in variables:
        if "units" in ds[v].attrs:
            if "yr" in ds[v].attrs["units"]:
                with xr.set_options(keep_attrs=True):
                    ds[v] = yr_to_s(ds[v], invert=True)
                    ds[v] = molC_to_g(ds[v])
                    ds[v] = g_to_kg(ds[v])
    return ds


def yr_to_s(da, invert=False):
    """Convert xr objects from year to kg/seconds."""
    if invert:  # if yr|s in denominator
        da = da / 3600 / 365.25
    else:
        da = da * 3600 * 365.25
    da.attrs["units"] = da.attrs["units"].replace("yr", "s")
    return da


def molC_to_g(da):
    """Convert xr objects from molC to g."""
    da = da * 12
    da.attrs["units"] = da.attrs["units"].replace("mol", "g")
    return da


def g_to_kg(da):
    """Convert xr objects from g to kg."""
    da = da / 1000
    da.attrs["units"] = da.attrs["units"].replace("g", "kg")
    return da
