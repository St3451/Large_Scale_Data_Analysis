#!/usr/bin/env python3
import sys

# Where do these lines come from?
# This is done by Hadoop Streaming ...
for line in sys.stdin:

    # Remove whitespace and split up line
    # into words (whitespace as delimiter)
    line = line.strip()
    words = line.split(",")
    
    if words[0][0] == "\"":
        continue
    
    if not len(words[6]):
        delay = 0
   
    else:
        delay = round(float(words[6]))
    
    airline_id = words[1]
    
    print('%s\t%s' % (airline_id, delay))