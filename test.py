#!/usr/bin/env python3
from html2image import Html2Image
#hti = Html2Image()
#with open('./test.html') as f:
#    hti.screenshot(f.read(), save_as='out.png')


hti = Html2Image("firefox", browser_executable="/usr/lib64/firefox")
hti.screenshot(url='https://cn.bing.com', save_as='bing.png')
