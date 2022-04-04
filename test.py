#!/usr/bin/env python3

import os
import re


s = r"""
\definefontsynonym[enserif][file:../../fonts/NotoSerif-Light.ttf]
\definefontsynonym[enserifbd][file:../../fonts/NotoSerif-SemiBold.ttf]
\definefontsynonym[enserifit][file:../../fonts/NotoSerif-LightItalic.ttf]
\definefontsynonym[enserifbi][file:../../fonts/NotoSerif-SemiBoldItalic.ttf]

\definefontfallback[nsecjkl][file:../../fonts/NotoSerifCJKtc-Light.otf][0x00400-0x2FA1F]
%\definefontfallback[nsecjkl][file:../../fonts/NotoSerifCJKtc-Light.otf][0x00400-0x2FA1F]
\definefontfallback[nsecjkb][file:../../fonts/NotoSerifCJKtc-Medium.otf][0x00400-0x2FA1F]
"""
print(s)

