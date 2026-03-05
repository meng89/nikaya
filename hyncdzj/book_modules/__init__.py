def _make_infos(ms):
    return [m.info for m in ms]


from . import sv, pv, kd
lv_ms = [sv, kd, pv]
lv_infos = _make_infos(lv_ms)


from . import dn, mn, sn, an
jing_ms = [dn, mn, sn, an]
jing_infos = _make_infos(jing_ms)


from . import kn_khp, kn_dhp, kn_ud, kn_iti, kn_snp, kn_vv, kn_pv, kn_thag, kn_thig, kn_ap, kn_jat, kn_ps, kn_bv, kn_cp, kn_nid1, kn_nid2
xiao_ms = [kn_khp, kn_dhp, kn_ud, kn_iti, kn_snp, kn_vv, kn_pv, kn_thag, kn_thig, kn_ap, kn_jat, kn_ps, kn_bv, kn_cp, kn_nid1, kn_nid2]
xiao_infos = _make_infos(xiao_ms)


from . import ds, vb, dt, pp, ya, patthana, kv
lun_ms = [ds, vb, dt, pp, ya, patthana, kv]
lun_infos = _make_infos(lun_ms)



from . import mil, dipavamsa, mahavamsa, culavamsa, visuddhimagga, samantapasadika, abhidhammatthasangaha, dhammalipi
wai_ms = [mil, dipavamsa, mahavamsa, culavamsa, visuddhimagga, samantapasadika, abhidhammatthasangaha, dhammalipi]
wai_infos = _make_infos(wai_ms)


all_modules = lv_ms + jing_ms + xiao_ms + lun_ms + wai_ms


module_tree = [
    ("律藏", lv_ms),
    ("經藏", [dn, mn, sn, an, ("小部", xiao_ms)]),
    ("論藏", lun_ms),
    ("藏外", wai_ms),
]

module_tree_test = [
    ("律藏", [sv]),
    ("經藏", [mn, sn, ("小部", xiao_ms[0:1])]),
    ("論藏", [ds]),
    ("藏外", wai_ms[0:1]),
]
