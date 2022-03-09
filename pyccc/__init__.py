import os

CCC_WEBSITE = "https://agama.buddhason.org"

TEX_DIR = PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

assert os.path.isdir(TEX_DIR)
