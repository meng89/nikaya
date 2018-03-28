#!/usr/bin/env python3
import os
from jinja2 import Template

from datetime import datetime
import config

books = []

for filename in sorted(os.listdir(config.BOOKS_DIR)):
    path = os.path.join(config.BOOKS_DIR, filename)
    book = {
        'filename': filename,
        'path': os.path.join(os.path.split(config.BOOKS_DIR)[1], filename),
        'size': '{:.1f} MB'.format(os.path.getsize(path) / (1024 * 1024)),
        'mtime': datetime.fromtimestamp(os.path.getmtime(path)).replace(microsecond=0),
    }

    books.append(book)

index_str = Template(open('index.html').read()).render(books=books)

open('../nikaya_gp/index.html', 'w').write(index_str)
