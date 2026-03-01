from . import sn, mn, dn, an
from . import kn

all_modules = [sn, mn, dn, an] + kn.all_modules


all_catalog = [
    ([], [sn.info, mn.info, dn.info, an.info]),
    (["小部"], [x.info for x in kn.all_modules])
]

module_tree = [
    sn,
    mn,
    dn,
    an,
    ("小部", kn.all_modules)
]

module_tree_test = [
    sn,
    mn,
    dn,
    an,
    ("小部", kn.all_modules[0:1])
]

def get_catalog_by_info(info):
    for catalog, infos in all_catalog:
        for info2 in infos:
            if info2 == info:
                return catalog
    raise Exception(info)


def get_catalog_by_module(module):
    for catalog, infos in all_catalog:
        for info2 in infos:
            if info2 == module.info:
                return catalog
    raise Exception(module)
