from . import sv, pv, kd

from . import kn_khp, kn_dhp, kn_ud, kn_iti, kn_snp, kn_vv, kn_pv, kn_thag, kn_thig, kn_ap, kn_jat, kn_ps, kn_bv, kn_cp, kn_nid1, kn_nid2
dh_modules = [kn_khp, kn_dhp, kn_ud, kn_iti, kn_snp, kn_vv, kn_pv, kn_thag, kn_thig, kn_ap, kn_jat, kn_ps, kn_bv, kn_cp, kn_nid1, kn_nid2]


def _make_infos(x):
    folder, ms = x
    return folder, [m.info for m in ms]

lv = (["律藏"], [sv, kd, pv])
lv_infos = _make_infos(lv)

from . import dn, mn, sn, an
jing = (["經藏"], [dn, mn, sn, an])
jing_infos = _make_infos(jing)

xiao = (["經藏", "小部"], dh_modules)
xiao_infos = _make_infos(xiao)
#jing = ("經藏", [sn])
from . import ds, vb, dt, pp, ya, patthana, kv
lun = (["論藏"], (ds, vb, dt, pp, ya, patthana, kv))
lun_infos = _make_infos(lun)

from . import mil, dipavamsa, mahavamsa, culavamsa, visuddhimagga, samantapasadika, abhidhammatthasangaha, dhammalipi
wai = (["藏外"], [mil, dipavamsa, mahavamsa, culavamsa, visuddhimagga, samantapasadika, abhidhammatthasangaha, dhammalipi])
wai_infos = _make_infos(wai)

categories = (jing, xiao, lv, lun, wai)

all_infos = (jing_infos, xiao_infos, lv_infos, lun_infos, wai_infos)

def _make_all_modules():
    _all_modules = []
    for _, ms in categories:
        for _m in ms:
            _all_modules.append(_m)
    return _all_modules

all_modules = _make_all_modules()


def get_classification(m):
    for c, ms in categories:
        if m in ms:
            return c
    raise Exception
