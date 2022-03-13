# 如果只是想自己制作电子书而不是开发此程序的话，需复制这个文件为 user_config.py，再修改复制后的文件。

import os.path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)


# 莊春江工作站目录
INDEX_DIR = "/mnt/data/Buddhism/ccc_2022.03.13/agama.buddhason.org/"

# 字体文件目录
FONTS_DIR = os.path.join(PROJECT_ROOT, "fonts")

# ConTeXt 目录
CONTEXT_BIN_PATH = "~/context-lmtx/tex/texmf-linux-64/bin"

# 电子书存放目录
BOOKS_DIR = os.path.join(PROJECT_ROOT, "fonts")
