#!/usr/bin/env python

import os
import re
import subprocess
import sys

mkvinfo = '/usr/bin/mkvinfo'

def get_size(mkv):
    try:
        size = os.path.getsize(mkv)
        return [size, size/1024/1024]
    except:
        return [0, 0]

def get_expected(mkv):
    try:
        output = subprocess.check_output([mkvinfo, '-z', mkv])
    except:
        return [0, 0]
    pattern = re.compile('^\+ .* size (\d+) data size.*$')
    size = 0
    for line in output.split('\n'):
        match = pattern.search(line.strip())
        if match:
            size += int(match.group(1))
    return [size, size/1024/1024]

def mkvcheck(mkv):
    size = get_size(mkv)
    expected = get_expected(mkv)
    if size[0] == 0 or expected[0] == 0:
        print 'Error: "%s" %d/%d MiB' % (mkv, size[1], expected[1])
        return
    if size[0] == expected[0]:
        print 'Good: "%s" %d/%d MiB' % (mkv, size[1], expected[1])
        return
    if size[0] != expected[0]:
        print 'Bad: "%s" %d/%d MiB' % (mkv, size[1], expected[1])

if len(sys.argv) < 2:
    print 'Error: Wrong number of arguments. Specify one or more files.'
    print 'Usage: ./mkvcheck.py FILE [FILE ...]'
    print 'Example: find . -iname "*.mkv" -print0 | xargs -0 ./mkvcheck.py'
    sys.exit(1)

for arg in sys.argv[1:]:
    mkvcheck(arg)
