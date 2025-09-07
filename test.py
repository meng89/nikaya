#!/usr/bin/env python3

from fpdf import FPDF

pdf = FPDF()
pdf.add_font("serif", "", "/mnt/data/projects/noto-cjk/Serif/OTF/TraditionalChinese/NotoSerifCJKtc-Regular.otf")
pdf.add_page()
pdf.set_font("serif", size=50)
pdf.multi_cell(text="我想看看尼奥是法拉盛会计法卢卡斯就立刻撒酒疯莱卡手机反拉是否极乐世界安乐死咖啡机阿斯利康街坊四邻杜可风就", w=330)
pdf.cell(text="你好世界，这是中文测试。萨菲林肯腊斯克继父卢卡斯记录卡手动继父莱卡继父莱卡健身房复礼克己仨莱卡手机莱卡手机的分离")
pdf.output("hello_world.pdf")
