#!/usr/bin/env python3

import os

import requests
from dateutil.parser import parse

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

url = "https://agama.buddhason.org/Su/Su31.htm"

response = requests.head(url) # Use HEAD request to get headers without downloading content
response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

if 'Last-Modified' in response.headers:
    last_modified_str = response.headers['Last-Modified']
    last_modified_date = parse(last_modified_str) # Parse the date string into a datetime object
    print(f"Last Modified Date: {last_modified_date}")
else:
    print("Last-Modified header not found in the response.")

path = "su31.htm"
with open(path, "wb") as f:
    r = requests.get(url, headers=headers)
    last_modified_str = r.headers['Last-Modified']
    print(last_modified_str)
    last_modified_date = parse(last_modified_str) # Parse the date string into a datetime object
    print(f"Last Modified Date: {last_modified_date}")
    os.utime(path, (new_mtime, new_mtime))
    f.write(r.content)
    print(r.ok)
