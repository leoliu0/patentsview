import csv
import sqlite3
import os
import zipfile as zip
from glob import glob
import numpy as np
import pandas as pd

file_name = "patent.tsv.zip"
f_name = "patent.tsv"

db = sqlite3.connect('patentsview.db')

for file_name in glob('*.zip'):
    f_name = file_name.split('.')[0]
    zf = zip.ZipFile(file_name)
    df = pd.read_csv(zf.open(file_name.rsplit('.',1)[0]), delimiter="\t",
                     quoting = csv.QUOTE_NONNUMERIC,low_memory=False)
    df.to_sql(f_name,db,index=False,if_exists='replace')
    print(f'finish processing {f_name}')
