#!/usr/bin/env python3
from lxml import etree
import sys

files = [
    'addons/matakuliah/views/matakuliah_views_clean.xml',
    'addons/matakuliah/views/matakuliah_menus.xml'
]

for f in files:
    try:
        tree = etree.parse(f)
        print(f"OK: {f}")
    except Exception as e:
        print(f"ERROR in {f}:")
        print(str(e))
        print()
