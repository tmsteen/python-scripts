#!/usr/bin/python3

##############################################################################
# Author: Trevor Steen
#
# Description: Script to consolidate test opnotes files from a team. Expects
# files with 'opnotes' in the name and RFC-3339 formated timestamps.
#
# Usage: Run in the directory with the opnotes files.
##############################################################################

import os
from datetime import datetime

# Remove old consolidated file if it exists
try:
    print('Removing old file...')
    os.remove('opnotes_consolidated.py')
except OSError:
    print ('No previous opnotes_consolidated.txt file found.')

# Constants
files = os.listdir(os.getcwd())
opnote_files = []
timed_lines = {}

# Get proper opnotes files
for i in files:
    if 'opnotes' in i.lower() and 'py' not in i.lower():
        opnote_files.append(i)
print('Found OpNotes files: \n' + '\n'.join(opnote_files))

# Timestamp placeholder so header type lines can get processed
timestamp = ''

# Go through each opnotes file
for i in opnote_files:
    individual_opnotes = open(i).readlines()
    for line in individual_opnotes:
        timestring = line.split('+')

        # See if the line starts with a timestamp and parse string into time object
        try:
            timestamp = datetime.strptime(timestring[0], '%Y-%m-%d %H:%M:%S')
            timed_lines[timestamp] = []
        except ValueError:
            pass

        # If there was a timestamp, get the first entry, otherwise, start writing other entries
        if timestamp:
            if len(timestring) > 1:
                # Get rid of extra newlines and leftover timezone
                timed_lines[timestamp].append(''.join(timestring[1:]).strip().strip('00:00 \t'))
            else:
                # Get rid of extra newlines
                timed_lines[timestamp].append(''.join(timestring[0:]).strip())

# Convert dict to list for sorting by time
entry_list = []
for entry in timed_lines:
    entry_list.append([entry, timed_lines[entry]])
entry_list.sort()

# Write output to file
with open('opnotes_consolidated.txt', 'w+') as consolidate:
    for entry in entry_list:
        # Write timestamp and first entry
        consolidate.write(entry[0].strftime('%Y-%m-%d %H:%M:%S') + '\t' * 3 + entry[1][0] + '\n')
        # Write all remaining entries
        for i in entry[1][1:]:
            consolidate.write('\t' * 7 + i + '\n')
        consolidate.write('\n\n')
