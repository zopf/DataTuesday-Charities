# This script preprocesses the results file saved from CharityCheck101.org,
# cleaning it into a form that can be easily processed by the next script.

import re

input_file_path = 'data/CharityCheck search results - CharityCheck101.org.html'
output_file_path = 'data/results_preprocessed.txt'

print 'Booting up...'
print 'Reading data from "%s"...' % input_file_path

# Match individual report urls in the file
result_re = re.compile(r'http://charitycheck101.org/report/\?id=[0-9]+')
matched_group_count = 0

# Find all matching URLs and write them to the output file
with open(input_file_path, 'r') as input_file:
  with open(output_file_path, 'w') as output_file:
    for line in input_file:
      matches = result_re.findall(line)
      for match in matches:
        matched_group_count += 1
        output_file.write('%s\n' % match)

print 'Processed %d results in input file.' % matched_group_count
print 'Finished.'