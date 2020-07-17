#!/usr/bin/env python3
import sys

total_count = 0
old_word = None
y_squared = 0
n = 0

# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:

    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        continue

    # Get word and count
    word, count = line

    try:
        count = int(count)
    except ValueError:
        print(word)
        continue

    # This if-statement only works because Hadoop sorts
    # the output of the mapping phase by key (here, by
    # word) before it is passed to the reducers. Each
    # reducer gets all the values for a given key. Each
    # reducer might get the values for MULTIPLE keys.
    if (old_word is not None) and (old_word != word):
        if n > 1:
            mean = total_count/n
            sd = ((1/(n-1))*y_squared - 1/(n-1)*(mean**2))**0.5
        else:
            mean, sd = total_count, 0   
        print('%s\t%s\t%s' % (old_word, mean, sd))
        total = 0
        y_squared = 0
        n = 0
    old_word = word
    total_count += count
    y_squared += count**2
    n += 1
    
# We have to output the word count for the last word!
if old_word is not None:
    if n > 1:
        mean = total_count/n
        sd = ((1/(n-1))*y_squared - 1/(n-1)*(mean**2))**0.5
    else:
        mean, sd = total_count, 0   
    print('%s\t%f\t%f' % (old_word, mean, sd))
