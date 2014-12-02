#!/bin/bash

# Run all the python files in order

# Pull the search result URLs from the CharityCheck101 search results page
# -- disabled for now --
# python preprocess_results.py

# Download the individual results pages - this takes a LONG time
# -- disabled for now --
# python download_individual_results.py

# Extract the individual results from the downloaded individual HTML files
python process_individual_results.py

# Transform the results to a format suitable for CartoDB
python prepare_for_cartodb.py
