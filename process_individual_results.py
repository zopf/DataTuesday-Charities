# This script lists the files in a directory and processes each one,
# fitting the data into a schema that can be stored in a database.

import re
import json
import csv
from os import listdir
from os.path import isfile, join

input_dir = 'data/downloads'
output_file_path = 'data/results_processed.txt'

# fields to read => where to store
content_mapping = {
  'Organization name' : 'Org_Name',
  'EIN (employer identification number)' : 'EIN',
  'Street address' : 'Street_Address',
  'City' : 'City',
  'State' : 'State',
  'ZIP' : 'ZIP',
  'Are donations deductible as charitable contributions?' : 'Are_Donations_Deductable',
  'Is the organization a Private Foundation?' : 'Is_Org_Private',
  'Organization is tax-exempt under this IRC subsection' : 'Subsection',
  'IRS ruling date (Month-Year)' : 'Ruling_Date',
  'Fiscal year ends (Month)' : 'Fiscal_Year_End',
  'Latest financial information reported to the IRS (Month-Year)' : 'Latest_Report',
  'Total assets reported' : 'Total_Assets',
  'Total revenues reported' : 'Total_Revenues',
  '"In Care Of" name shown in latest financial report to the IRS' : 'In_Care_Of'
}

# utility function for grepping out individual fields
def fetch_field (field, haystack):
  # example:
  # <td class="tal">"In Care Of" name shown in latest financial report to the IRS</td><td class="tac"><div id="incareofanwser">% WILLIAM KING</div><td>
  pattern = r'<td class="tal">\s*%s\s*</td>.*?<td class="tac">\s*(.*?)\s*</td>' % re.escape(field)
  # some special cases, probably ought to be encoded as a dict, ah well
  if field.startswith('"In Care Of"'):
    pattern = r'<td class="tal">\s*%s\s*</td>.*?<td class="tac">\s*<div id="incareofanwser">\s*(.*?)\s*</div>\s*<td>' % re.escape(field) # note, unclosed td
  elif field.startswith('EIN'):
    pattern = r'<td class="tal">\s*%s\s*</td>.*?<td class="tac">\s*<strong>\s*<font color ="red">\s*(.*?)\s*</font>\s*</strong>\s*</td>' % re.escape(field)
  match = re.search(pattern, haystack)
  if match:
    return match.group(1)
  return None

# utility function for grepping out full object
def fetch_object (haystack):
  obj = {}
  for key in content_mapping.keys():
    obj_key = content_mapping[key]
    obj[obj_key] = fetch_field(key, haystack)
  return obj

print 'Booting up...'
print 'Iterating over all files in %s...' % input_dir

# set up loop state
input_file_names = [ f for f in listdir(input_dir) if isfile(join(input_dir,f)) ]
processed_files_count = 0
wrote_header = False
header_keys = []

with open(output_file_path, 'w') as output_file:
  csvwriter = csv.writer(output_file)
  for input_file_name in input_file_names:
    input_file_path = join(input_dir,input_file_name)
    with open(input_file_path, 'r') as input_file:
      clean_content = input_file.read().replace('\n', '')
      processed_files_count += 1
      result = fetch_object(clean_content)
      # # JSON output
      # output_file.write(json.dumps(result, sort_keys=True))
      # output_file.write('\n')
      # CSV output
      if not wrote_header:
        header_keys = content_mapping.values()
        header_keys.sort()
        csvwriter.writerow(header_keys)
        wrote_header = True
      csvwriter.writerow([result[key] for key in header_keys])

print 'Processed %d input files from %s.' % (processed_files_count, input_dir)
print 'Wrote results to %s.' % output_file_path
print 'Finished.'