#!/bin/sh
wget -i $(lynx -dump https://www.patentsview.org/download/ | grep .zip | cut -d' ' -f4)
unzip -o \*.zip

python to_sqlite.py
