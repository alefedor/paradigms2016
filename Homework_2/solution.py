import sys
import os
from os import walk
from hashlib import sha1
from collections import defaultdict


def read_filepaths(folder):
    for path, _, files in walk(folder):
        for f in files:
            if f.startswith('.') or f.startswith('~'):
                continue
            filepath = os.path.join(path, f)
            yield filepath


def get_hash(document):
    h = sha1()
    with open(document, "rb") as f:
        while (True):
            s = f.read(1024*4)
            if not s:
                break
            h.update(s)
    return h.hexdigest()


def print_equal(folder):
    files = read_filepaths(folder)
    d = defaultdict(list)
    for document in files:
        h = get_hash(document)
        d[h].append(document)
    for lst in d.values():
        if len(lst) > 1:
            print(':'.join(lst))


def main():
    if len(sys.argv) != 2:
        print("usage: ./solution.py dir")
        sys.exit(1)
    folder = sys.argv[1]
    print_equal(folder)


if __name__ == '__main__':
    main()