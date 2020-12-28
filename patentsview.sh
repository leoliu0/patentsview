#!/bin/sh
lynx -dump https://www.patentsview.org/download/ | grep -Po 'http.*tsv.zip' > list_of_files.txt

wget -N -i list_of_files.txt

python to_sqlite.py
