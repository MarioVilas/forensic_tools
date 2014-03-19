#!/usr/bin/env python

# A simple char count utility in Python.
# By Mario Vilas (mvilas at gmail dot com)

# It's basically a 5-minute reimplementation of this, just to mess with Capi_X a bit ;)
# https://bitbucket.org/capi_x/jr-tools/src/385fea5bdc4fed36969dfff4c165e470265361d0/cntchar.c?at=default

# Turns out this version is ~500x times slower on CPython for small
# files (expected), but a little faster on >2Mb files (surprise!).

from collections import Counter
from math import ceil
from sys import argv

with open(argv[0], 'rU') as f:
    c = Counter( f.read() )
t = sum( c.values() )
s = sorted( (v, k) for (k, v) in c.iteritems() )
print "COUNT   CHAR    PCENT   GRAPH"
print "----------------------------------"
for v, k in s:
    p = int(ceil(float(v * 100) / t))
    print "%-7d %-7r %-7s %s" % (v, k, "%s%%" % p, "X" * p)
