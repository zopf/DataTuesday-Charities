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

CartoDBing
---
Here's how we transform the raw uploaded data to the aggregated results for the chart:
```
SELECT the_geom, the_geom_webmercator,
COUNT(*) AS charity_count,
FLOOR(MAX(total_revenues)) AS max_total_revenues,
FLOOR(MAX(total_assets)) AS max_total_assets,
FLOOR(SUM(total_revenues)) AS sum_total_revenues,
FLOOR(SUM(total_assets)) AS sum_total_assets,
FLOOR(AVG(total_revenues)) AS avg_total_revenues,
FLOOR(AVG(total_assets)) AS avg_total_assets 
FROM charitycheck101_scrape_nyc 
WHERE subsection = '501(c)(3)' AND total_revenues > 0
GROUP BY the_geom, the_geom_webmercator
```
