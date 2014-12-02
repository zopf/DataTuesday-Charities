DataTuesday-Charities
=====================

The code for Alec Zopf's DataTuesday project focusing on charities - 2014-12-02

Goal
---
The goal of this project is to get financial information about every charity in NYC and examine that data on a map.

Results
---
Don't bury the lede!  Here are the results on CartoDB: http://cdb.io/1tJwycX

Implementation
---
We're using Python scripts to scrape CharityCheck101.org's search results for NYC, fetching each HTML result document and later parsing them to extract relevant details.  Then, we're tweaking the data and uploading it to CartoDB, where we'll run some SQL queries to aggregate and visualize the results.

How You'd Run It
---
Look at the `run_it_all.sh` file to, well, run it all.  To actually enable the downloading of all HTML result files (which takes hours and totals over a gigabyte of downloaded content), you'll need to uncomment a couple lines.  But don't worry, all the data you'd get is already munged and included in the `results_processed.txt` file.
