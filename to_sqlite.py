#!/bin/python
import argparse
import asyncio
import csv
import os
import re
import sqlite3
import sys
import urllib
import zipfile as zip
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger

import pandas as pd
import requests

if __name__ != "__main__":
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--small", action="store_true")
parser.add_argument("--additional", action="store_true")
parser.add_argument("-j", type=int)
parser.add_argument("-k", "--keep", action="store_true")
args = parser.parse_args()
jobs = args.j if args.j else None

db = sqlite3.connect("patentsview.db")
website = requests.get(
    "https://patentsview.org/download/data-download-tables").text.split()


def download(url):
    url = re.findall("http.*\.tsv\.zip", url)[0]
    fn = url.split("/")[-1].split(".")[0]
    logger.info(url, fn)
    if args.small:
        if "desc.tsv.zip" in url:
            return
    newfn = fn + ".tsv.zip"
    urllib.request.urlretrieve(url, newfn)
    return fn


with ThreadPoolExecutor() as executor:
    downloaded = []
    for url in website:
        if re.search("http.*\.tsv\.zip", url):
            downloaded.append(executor.submit(download, url))

    for fn in as_completed(downloaded):
        fn = fn.result()
        df = pd.read_csv(
            fn + '.tsv.zip',
            delimiter="\t",
            quoting=csv.QUOTE_NONNUMERIC,
            low_memory=False,
        )
        df.to_sql(fn, db, index=False, if_exists="replace")
        if not args.keep:
            os.remove(fn + '.tsv.zip')

if args.additional:
    url = "https://bulkdata.uspto.gov/data/patent/maintenancefee/MaintFeeEvents.zip"
    logger.info(url)
    try:
        urllib.request.urlretrieve(url)
    except:
        logger.warning("unable to get maintenance fee event")
