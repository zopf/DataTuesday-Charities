# This script imports the processed results and convets them to
# a format that is suitable for use with CartoDB

import csv
import locale
locale.setlocale(locale.LC_ALL, '')

input_file_path = 'data/results_processed.txt'
output_file_path = 'data/results_processed.forcartodb.txt'

print 'Booting up...'
print 'Processing data for CartoDB from %s...' % input_file_path

processed_record_count = 0

# prep the reader
with open(input_file_path, 'r') as input_file:
  reader = csv.DictReader(input_file)
  fieldnames = reader.fieldnames
  # prep the writer
  with open(output_file_path, 'w') as output_file:
    writer = csv.DictWriter(output_file, fieldnames)
    writer.writeheader()
    # iterate over records, transforming them as necessary
    for row in reader:
      processed_record_count += 1
      # slice the zip to 5 digits
      zip9 = str(row['ZIP'])
      zip5 = zip9[0:5] if zip9 else None
      row['ZIP'] = zip5
      # turn money into integers
      row['Total_Assets'] = locale.atof(row['Total_Assets'][1:]) if row['Total_Assets'] else 0
      row['Total_Revenues'] = locale.atof(row['Total_Revenues'][1:]) if row['Total_Revenues'] else 0
      # write out the modified row
      writer.writerow(row)

print 'Processed %d records into %s.' % (processed_record_count, output_file_path)
print 'Finished.'