import intake


def cmor_cat(cat="../master.yml", keyword="cmor", depth=3):
    if isinstance(cat, str):
        cat = intake.open_catalog(cat)
    assert isinstance(cat, intake.catalog.local.YAMLFileCatalog)  # type: ignore[attr-defined]
    return intake.Catalog.from_dict(cat.search(keyword, depth=depth).walk())  # type: ignore[call-arg, union-attr]
