#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys


def get_size(mkv):
    try:
        size = os.path.getsize(mkv)
        return [size, size/1024/1024]
    except (FileNotFoundError, PermissionError):
        return [0, 0]


def get_expected(mkv):
    try:
        output = subprocess.check_output([mkvinfo, '-z', mkv])
    except subprocess.CalledProcessError:
        return [0, 0]
    pattern = re.compile(r'^\+ .* size (\d+)$')
    size = 0
    for line in output.decode().split('\n'):
        line = line.strip()
        # for mkvtoolnix >= v32.0.0: remove data size
        if ' data size' in line:
            line = line[:line.find(' data size')]
        match = pattern.search(line)
        if match:
            size += int(match.group(1))
    return [size, size/1024/1024]


def mkvcheck(mkv):
    size = get_size(mkv)
    expected = get_expected(mkv)
    if size[0] == 0 or expected[0] == 0:
        print('Error: {} {:.2f}/{:.2f} MiB'.format(mkv, size[1], expected[1]))
        return
    if size[0] == expected[0]:
        print('Good: {} {:.2f} MiB'.format(mkv, size[1]))
        return
    if size[0] != expected[0]:
        print('Bad: {} {:.2f}/{:.2f} MiB'.format(mkv, size[1], expected[1]))


if len(sys.argv) < 2:
    print('Error: Wrong number of arguments. Specify one or more files.\n'
          'Usage: ./mkvcheck.py FILE [FILE ...]\n'
          'Example: find . -iname "*.mkv" -print0 | xargs -0 ./mkvcheck.py')
    sys.exit(1)

mkvinfo = shutil.which('mkvinfo')
if not mkvinfo:
    print('Error: mkvinfo not found. Install mkvtoolnix.')
    sys.exit(1)

for arg in sys.argv[1:]:
    mkvcheck(arg)
