from __future__ import print_function
import os
import re
import sys
from collections import defaultdict

if __name__ == '__main__':
    bytes_to_megabytes_factor = 1.0 / (1024 * 1024)

    # Get path to search for ANSYS projects under
    if len(sys.argv) < 2:
        print("Usage: {} <path that includes ANSYS projects>".format(sys.argv[0]))
        sys.exit(1)
    rootdir = sys.argv[1]

    # Generate dictionary of ANSYS file extension patterns mapped to 
    # corresponding compiled regexes
    file_type_patterns = {}
    with open('ansys_audit.csv', 'r') as f:
        for line in f:
            ext_pat = line.split('|')[0] \
                          .replace('n', '[0-9]') \
                          .replace('x', '[0-9]') \
                          .lower()
            file_type_patterns[ext_pat] = re.compile(".*\.{}$".format(ext_pat))

    # Trawl the filesystem under rootdir and log the amount of space used per file type
    sizes_per_file_type = defaultdict(lambda: 0)
    for root, subdirs, files in os.walk(rootdir):
        for f in files:
            for ft in file_type_patterns:
                if file_type_patterns[ft].match(f.lower()):
                    file_path = os.path.join(root, f)
                    sizes_per_file_type[ft] += (os.path.getsize(file_path) * bytes_to_megabytes_factor)
                    break

    # Print amount of space used per file type
    for ft in sorted(sizes_per_file_type, key=sizes_per_file_type.get, reverse=True):
         print(ft, sizes_per_file_type[ft])
