import epubpacker
import xml.etree.ElementTree as ET

import pyccc.pdf
from pyccc import sn


def write_suttas(epub, bns, c, test=False):
    nikaya = sn.get()
    p = ET.Element("html")

    for pian in nikaya.pians:
        ET.SubElement(p, "h1").text = c(pian.title)

        for xiangying in pian.xiangyings:
            ET.SubElement(p, "h2").text = c(xiangying.serial + ". " + xiangying.title)

            for pin in xiangying.pins:
                if pin.title is not None:
                    ET.SubElement(p, "h3").text = c(pin.title)

                for sutta in pin.suttas:
                    ET.SubElement(p, "h4").text = c(sutta.title)
                    for body_listline in sutta.body_lines:
                        p.extend(pyccc.pdf.join_to_xml(body_listline))


