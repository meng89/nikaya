import os
import pickle


from . import mn
from . import sn


_all_data = {}


_xn2module = {"sn": sn,
              "mn": mn
              }


def load(xn, domain, cache_dir):
    nikaya_module = _xn2module[xn]
    global _all_data
    data_path = os.path.join(cache_dir, xn)
    try:
        with open(data_path, "rb") as rf:
            _nikaya = pickle.load(rf)
    except (FileNotFoundError, ModuleNotFoundError):
        _nikaya = nikaya_module.make_nikaya(domain)
        with open(data_path, "wb") as wf:
            pickle.dump(_nikaya, wf)
    _all_data[xn] = _nikaya


def get(xn):
    return _all_data[xn]

