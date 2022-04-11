#!/usr/bin/env python3

from html2image import Html2Image as HtI
hti = HtI(browser_executable="google-chrome-stable")
hti.screenshot(html_str=open("cover.xhtml").read(), size=(1600, 2560), save_as="cover.png")

