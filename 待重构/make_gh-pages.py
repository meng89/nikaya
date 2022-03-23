#!/usr/bin/env python3
import os
from jinja2 import Template

from datetime import datetime
import user_config

books = []

for filename in sorted(os.listdir(config.EPUB_DIR)):
    path = os.path.join(config.EPUB_DIR, filename)
    book = {
        'filename': filename,
        'package_opf_path': os.path.join(os.path.split(config.EPUB_DIR)[1], filename),
        'size': '{:.1f} MB'.format(os.path.getsize(path) / (1024 * 1024)),
        'mtime': datetime.fromtimestamp(os.path.getmtime(path)).replace(microsecond=0),
    }

    books.append(book)

index_str = Template(open('xhtml/index.html').read()).render(books=books)

open('../nikaya_gp/index.html', 'w').write(index_str)
