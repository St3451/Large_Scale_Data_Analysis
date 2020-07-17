#!/usr/bin/env python3
import sys

old_top10 = [0 for _ in range(10)]
old_word = None

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
        print('%s\t%s' % (old_word, old_top10))
        old_top10 = [0 for _ in range(10)]
    
    for j in range(0, len(old_top10)):
        if count > old_top10[j]:
            old_top10[j] = count
            old_top10.sort()
            break
        else:
            continue
            print("value is", old_top10[j])

    old_word = word

# We have to output the word count for the last word!
if old_word is not None:
    print('%s\t%s' % (old_word, old_top10))
