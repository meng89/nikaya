import os.path

from pyccc.utils import PROJECT_ROOT

# 莊春江工作站下载的全站打包文件(pyccc.rar)解压后的目录, 此目录下
INDEX_DIR = "/mnt/data/Buddhism/ccc/agama.buddhason.org/"

# 程序生成的 epub 存放目录
BOOKS_DIR = "../books"

FONTS_DIR = os.path.join(PROJECT_ROOT, "fonts")

CONTEXT_BIN_PATH = "~/context-lmtx/tex/texmf-linux-64/bin"
