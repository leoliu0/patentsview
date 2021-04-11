import sqlite3
import os
import re
import csv
import zipfile as zip
import pandas as pd
import requests

db = sqlite3.connect('patentsview.db')
website = requests.get('https://patentsview.org/download/data-download-tables').text.split()

for x in website:
    if re.search('http.*\.tsv\.zip',x):
        url = re.findall('http.*\.tsv\.zip',x)[0]
        fn = url.split('/')[-1].split('.')[0]
        print(url, fn)
        df = pd.read_csv(url,delimiter="\t",quoting = csv.QUOTE_NONNUMERIC,low_memory=False)
        df.to_sql(fn,db,index=False,if_exists='replace')
