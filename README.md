# patentsview
Python scripts to process the patentviews data and create a sqlite database

* Prerequisites
1. python3.6+ with pandas installed
2. 32GB+ memory if you want to calculate patent metrics

* Usage:
```Python
python to_sqlite.py
```
* If you need to compute some standardard patent metrics, you can run
```Python
python calculate_patent_stats.py
```
This will calculate some simple metrics based on USPC.

Or you can go to OECD to obtain their measures, or go to my google-patent repo to obtain my constructed measure following OECD guidelines (with minor difference in parameters)
