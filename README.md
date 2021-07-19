# patentsview
Python scripts to process the patentviews data and create a sqlite database

* Prerequisites
1. python3.6+ with pandas installed. Run
```Bash
pip install -r requirements.txt
```
to install required packages
2. 32GB+ memory if you want to calculate patent metrics

* Usage:
```Python
python to_sqlite.py
```
```Python
python to_sqlite.py --small
```
To avoid download description files which are large and make the database slow

```Python
python to_sqlite.py --additional
```
To download maintainence fee events for calculating patent life

* If you need to compute some standardard patent metrics, you can run
```Python
python calculate_patent_stats.py
```
This will calculate some simple metrics based on USPC.

Or you can go to OECD to obtain their measures, or go to my google-patent repo to obtain my constructed measure following OECD guidelines (with minor difference in parameters)
