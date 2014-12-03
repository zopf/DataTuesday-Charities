# This script reads URLs from the input file, one by one, downloading
# them and saving them into the output directory, with filenames corresponding
# to the EIN of the organization.

import urllib2
import re
import os

input_file_path = 'data/results_preprocessed.txt'
output_file_base_path = 'data/downloads/'

url_ein_re = re.compile(r'http://charitycheck101.org/report/\?id=([0-9]+)')

print 'Booting up...'
print 'Processing URLs from file %s...' % input_file_path

processed_result_count = 0
print_interval = 100

with open(input_file_path, 'r') as input_file:
  # for each URL
  for line in input_file:
    # periodic printouts
    processed_result_count += 1
    if processed_result_count % print_interval == 0:
      print '%d result URLs downloaded...' % processed_result_count
    # ensure that url is valid
    if not url_ein_re.match(line):
      continue
    # path builing
    ein = url_ein_re.search(line).group(1) # extract the EIN from the url
    output_file_path = '%s%s.html' % (output_file_base_path, ein)
    # skip if we'e already downloaded this file
    if os.path.isfile(output_file_path):
      continue
    # download the URL
    try:
      response = urllib2.urlopen(line)
      html = response.read()
      # save it to the appropriate output file
      with open(output_file_path, 'w') as output_file:
        output_file.write(html)
    except:
      print "Failed to download %s: %s" % ( line, sys.exc_info()[0] )

print 'Done downloading %d result URLs.' % processed_result_count
print 'Finished.'
