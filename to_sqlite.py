#!/bin/python
import argparse
import csv
import os
import re
import sqlite3
import sys
import urllib
import zipfile as zip
from concurrent.futures import ProcessPoolExecutor, as_completed
from loguru import logger

import pandas as pd
import requests

if __name__ != "__main__":
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--small", action="store_true")
parser.add_argument("--additional", action="store_true")
parser.add_argument("-j", type=int)
args = parser.parse_args()
jobs = args.j if args.j else None

db = sqlite3.connect("patentsview.db")
website = requests.get(
    "https://patentsview.org/download/data-download-tables"
).text.split()


def download(url):
    url = re.findall("http.*\.tsv\.zip", url)[0]
    fn = url.split("/")[-1].split(".")[0]
    logger.info(url, fn)
    if args.small:
        if "desc.tsv.zip" in url:
            return
    try:
        df = pd.read_csv(
            url,
            delimiter="\t",
            quoting=csv.QUOTE_NONNUMERIC,
            low_memory=False,
        )
    except:
        logger.warning(f"Read {fn} directly failed! Download the file instead")
        newfn = fn + ".tsv.zip"
        urllib.request.urlretrieve(url, newfn)
        df = pd.read_csv(
            newfn,
            delimiter="\t",
            quoting=csv.QUOTE_NONNUMERIC,
            low_memory=False,
        )
        os.remove(newfn)
    return df, fn


with ProcessPoolExecutor(max_workers=jobs) as executor:
    if not jobs:
        jobs = "all"
    logger.info(f"Running jobs using {jobs} cores")
    dfs = []
    for url in website:
        # if re.search("http.*\.tsv\.zip", url):
        if re.search("http.*\.tsv\.zip", url):
            dfs.append(executor.submit(download, url))

    for res in as_completed(dfs):
        df, fn = res.result()
        df.to_sql(fn, db, index=False, if_exists="replace")

if args.additional:
    url = "https://bulkdata.uspto.gov/data/patent/maintenancefee/MaintFeeEvents.zip"
    logger.info(url)
    try:
        urllib.request.urlretrieve(url)
    except:
        logger.warning("unable to get maintenance fee event")
