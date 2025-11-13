from . import sv, pv, kd

from . import kn_khp, kn_dhp, kn_ud, kn_iti, kn_snp, kn_vv, kn_pv, kn_thag, kn_thig, kn_ap, kn_jat, kn_ps, kn_bv, kn_cp, kn_nid1, kn_nid2
dh_modules = [kn_khp, kn_dhp, kn_ud, kn_iti, kn_snp, kn_vv, kn_pv, kn_thag, kn_thig, kn_ap, kn_jat, kn_ps, kn_bv, kn_cp, kn_nid1, kn_nid2]


lv = ("律藏", [sv, kd, pv])

from . import dn, mn, sn, an
jing = ("經藏", [dn, mn, sn, an] + dh_modules)
jing = ("經藏", [sn])
from . import ds, vb, dt, pp, ya, patthana, kv
lun = ("論藏", (ds, vb, dt, pp, ya, patthana, kv))

from . import mil, dipavamsa, mahavamsa, culavamsa, visuddhimagga, samantapasadika, abhidhammatthasangaha, dhammalipi
wai = ("藏外", [mil, dipavamsa, mahavamsa, culavamsa, visuddhimagga, samantapasadika, abhidhammatthasangaha, dhammalipi])

categories = (lv, jing, lun, wai)
categories = (jing, )