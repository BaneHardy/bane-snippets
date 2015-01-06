#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    print 'Error: Wrong number of arguments. Specify one or more files or empty directories.'
    print 'Usage: ./unlink.py FILE [FILE ...]'
    print 'Deletes FILE but preserves atime and mtime of the parent directory.'
    print 'Example: find /dir/ -name "file" -print0 | xargs -0 ./unlink.py'
    print 'Example: find /dir/ -type d -empty -print0 | xargs -0 ./unlink.py'
    sys.exit(1)

def unlink(filename):
    try:
        filename = os.path.normpath(filename)
        parent = os.path.dirname(filename)
        parent_stat = os.stat(parent)
        if os.path.isdir(filename):
            os.rmdir(filename)
        if os.path.isfile(filename):
            os.unlink(filename)
        os.utime(parent, (parent_stat.st_atime, parent_stat.st_mtime))
    except:
        print 'Error: "%s" caused problems.' % filename

for arg in sys.argv[1:]:
    unlink(arg)
