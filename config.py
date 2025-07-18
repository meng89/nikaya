# 如果只是想自己制作电子书而不是开发此程序的话，需复制这个文件为 user_config.py，再修改复制后的文件。

import os.path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)



# 莊春江工作站目录
INDEX_DIR = "/mnt/data/Buddhism/abo_2025.07.09/agama.buddhason.org/"
# INDEX_DIR = r"D:\abo_2022.03.34\agama.buddhason.org\"


_RESOURCE_DIR = os.path.join(PROJECT_ROOT, "resource")

DOWNLOAD_DIR = os.path.join(_RESOURCE_DIR, "htm")
XML_DIR = os.path.join(_RESOURCE_DIR, "xml")

TIMESTAMP = os.path.join(_RESOURCE_DIR, "timestamp.csv")

SOCKS5_PROXY = "127.0.0.1:1080"
#SOCKS5_PROXY = None
# 经文缓存目录
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")

# 字体文件目录
# FONTS_DIR = os.path.join(PROJECT_ROOT, "fonts")
FONTS_DIR = "/mnt/data/software/fonts"
# FONTS_DIR = r"D:\fonts"

# ConTeXt 目录
CONTEXT_BIN_PATH = "~/context-lmtx/tex/texmf-linux-64/bin"
# CONTEXT_BIN_PATH = r"D:\context-win64\tex\texmf-win64\bin"

# EPUBCheck 路径
EPUBCHECK = "/mnt/data/software/epubcheck-5.2.1/epubcheck.jar"
# EPUBCHECK = r"D:\epubcheck-4.2.6\epubcheck.jar"

# 电子书存放目录
BOOKS_DIR = os.path.join(PROJECT_ROOT, "_books")

LOG_PATH = os.path.join(PROJECT_ROOT, "abo_log.txt")
