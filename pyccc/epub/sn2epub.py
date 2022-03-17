import epubpacker

from pyccc import sn


def write_suttas(epub, bns, c, test=False):
    nikaya = sn.get()

    for pian in nikaya.pians:

        for xiangying in pian.xiangyings:

            for pin in xiangying.pins:
                if pin.title is not None:

                for sutta in pin.suttas:

                    for body_listline in sutta.body_lines:
                        
