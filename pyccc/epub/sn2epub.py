import xl

import pyccc.pdf
from pyccc import sn


def write_suttas(epub, bns, c, test=False):
    nikaya = sn.get()
    p = xl.Element("html")

    for pian in nikaya.pians:
        xl.sub(p, "h1", kids=[c(pian.title)])

        for xiangying in pian.xiangyings:
            xl.sub(p, "h2", kids=[c(xiangying.serial + ". " + xiangying.title)])

            for pin in xiangying.pins:
                if pin.title is not None:
                    xl.sub(p, "h3", kids=[c(pin.title)])

                for sutta in pin.suttas:
                    xl.sub(p, "h4", kids=[c(sutta.title)])
                    for body_listline in sutta.body_lines:
                        p.kids.extend(pyccc.pdf.join_to_xml(body_listline, c))
