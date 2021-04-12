import sqlite3
import os
import re
import csv
import zipfile as zip
import pandas as pd
import requests
import urllib

db = sqlite3.connect('patentsview.db')
website = requests.get('https://patentsview.org/download/data-download-tables').text.split()

for x in website:
    if re.search('http.*\.tsv\.zip',x):
        url = re.findall('http.*\.tsv\.zip',x)[0]
        fn = url.split('/')[-1].split('.')[0]
        print(url, fn)
        try:
            df = pd.read_csv(url,delimiter="\t",quoting = csv.QUOTE_NONNUMERIC,low_memory=False)
        except:
            newfn = fn+'.tsv.zip'
            urllib.request.urlretrieve (url, newfn)
            df = pd.read_csv(newfn,delimiter="\t",quoting = csv.QUOTE_NONNUMERIC,low_memory=False)
            os.remove(newfn)
        df.to_sql(fn,db,index=False,if_exists='replace')
