# patentsview
patentview scripts to process the data

* Prerequisites
1. standard GNU utilities: wget, zip, grep, lynx
2. python3.6+ with pandas installed
3. 32GB+ memory

* Usage:
```bash
./patentview.sh
```
* If you need to compute some standardard patent metrics, you can run
```bash
python calculate_patent_stats.py
```
This will calculate some simple metrics based on USPC.

Or you can go to OECD to obtain their measures, or go to my google-patent repo to obtain my constructed measure following OECD guidelines (with minor difference in parameters)
