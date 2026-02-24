from . import sn, mn, dn, an
from . import kn

all_modules = [sn, mn, dn, an] + kn.all_modules


all_catalog = []


for x  in [sn, mn, dn, an]:
    all_catalog.append(([], x.info))


for x in kn.all_modules:
    all_catalog.append((["小部"], x.info))


def get_catalog_by_info(info):
    for catalog, info2 in all_catalog:
        if info2 == info:
            return catalog
    raise Exception(info)


def get_catalog_by_module(module):
    for catalog, info2 in all_catalog:
        if info2 == module.info:
            return catalog
    raise Exception(module)