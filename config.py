import os.path


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ABO_WEBSITE = "https://agama.buddhason.org"


RESOURCE_DIR = os.path.join(PROJECT_ROOT, "resource")

ABO_RESOURCE_DIR = os.path.join(RESOURCE_DIR, "abo")
ABO_COVER_DIR = os.path.join(ABO_RESOURCE_DIR, "cover")
ABO_DOWNLOAD_DIR = os.path.join(ABO_RESOURCE_DIR, "htm")
ABO_XML_DIR = os.path.join(ABO_RESOURCE_DIR, "xml")

ABO_TEX_DIR = os.path.join(PROJECT_ROOT, "abo", "tex")
HYNCDZJ_TEX_DIR = os.path.join(PROJECT_ROOT, "hyncdzj", "tex")
HYNCDZJ_RESOURCE_DIR = os.path.join(RESOURCE_DIR, "hyndzj")
HYNCDZJ_COVER_DIR = os.path.join(HYNCDZJ_RESOURCE_DIR, "cover")
SIMPLE_DOC_DIR = os.path.join(HYNCDZJ_RESOURCE_DIR, "simple_doc")
SIMPLE_FILLING_DIR = os.path.join(HYNCDZJ_RESOURCE_DIR, "simple_充填中")
os.makedirs(SIMPLE_FILLING_DIR, exist_ok=True)
SIMPLE_FILLED_DIR = os.path.join(HYNCDZJ_RESOURCE_DIR, "simple_充填完成")
os.makedirs(SIMPLE_FILLED_DIR, exist_ok=True)

SOCKS5_PROXY = "127.0.0.1:1080"
#SOCKS5_PROXY = None
# 经文缓存目录

# 字体文件目录，具体的字体文件可以在这些目录的某个文件夹下
# FONTS_DIR = os.path.join(PROJECT_ROOT, "fonts")
FONTS_DIRS = [
    "/usr/share/fonts/arphicfonts",
    "/mnt/data/software/fonts",
]
# FONTS_DIR = r"D:\fonts"

# ConTeXt 目录
CONTEXT_BIN_PATH = "/mnt/data/software/context"
# CONTEXT_BIN_PATH = r"D:\context-win64\tex\texmf-win64\bin"

# EPUBCheck 路径
EPUBCHECK = "/mnt/data/software/epubcheck-5.2.1/epubcheck.jar"
# EPUBCHECK = r"D:\epubcheck-4.2.6\epubcheck.jar"

XMLP5A_DIR = "/mnt/data/projects/xml-p5a/"


LOG_PATH = os.path.join(PROJECT_ROOT, "abo_log.txt")

#BROWSER = "/opt/firefox/firefox"
BROWSER = "google-chrome-stable"
#BROWSER = "microsoft-edge-stable"
WINDOW_HEIGHT_OFFSET = 86


DEBUG = True
