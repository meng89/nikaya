from . import sn, mn, dn, an
from . import kn

all_modules = [sn, mn, dn, an] + kn.all_modules

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
    ("小部", kn.all_modules[0:1])
]