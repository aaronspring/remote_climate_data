import os
import fsspec
import intake_geopandas
import intake

def cache_all_catalog_items(cat, cache_storage=None):
    """Cache all catalog items from catalog `cat` that contain `cache::` in url to folder optionally specified by `cache_storage`.

    Example:
        >>> cat = intake.open_catalog('master.yaml')
        >>> cache_all_catalog_items(cat, 'test_cache_folder')
        >>> os.path.exists('test_cache_folder/HadCRUT.4.6.0.0.median.nc')
    """
    fsspec.config.conf['simplecache']={'same_names': True}
    if cache_storage:
        fsspec.config.conf['simplecache']={'cache_storage': cache_storage, 'same_names':True}
        print('fsspec.config.conf',fsspec.config.conf,'\n')
    for item_str in cat.walk(depth=2):
        if 'CRU_TS' not in item_str:
            item = getattr(cat, item_str)
            if not isinstance(cat[item_str],intake.catalog.local.YAMLFileCatalog):
                if 'cache::' in item.urlpath:
                    filename = item.urlpath.split('/')[-1]
                    print(f'try to cache {item_str} from {item.urlpath} to {cache_storage}/{filename}')
                    try:
                        if isinstance(item, (intake_geopandas.RegionmaskSource, intake_geopandas.GeoPandasFileSource)):
                            ds = item.read()
                            print(item_str, '\n',type(item), '\n', ds.dims, '\n', ds.coords, '\nsize = ', format_bytes(ds.nbytes))
                        else:
                            ds = item.to_dask()
                            print(item_str, '\n',type(item))
                        if cache_storage:
                            assert filename in os.listdir(f'{cache_storage}'), print(item_str,'caching failed:',os.listdir(cache_storage))
                        print('successful', item_str,'\n')
                    except Exception as e:
                        print(f'{item_str} failed, error {type(e).__name__}: {e}\n')
