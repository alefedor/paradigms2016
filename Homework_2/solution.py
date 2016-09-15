import sys
import os
from os import walk
from hashlib import sha1

dict = dict()

def read_filepaths(dir):
    for path, _, files in walk(dir):
        for f in files:
            if f[0] == '.' or f[0] == '~':
                continue
            filepath = os.path.join(path, f)
            yield filepath


def get_hash(file):
    h = sha1()
    with open(file, "rb") as f:
        while (True):
            s = f.read(1024*4)
            if not s:
                break
            h.update(s)
    return h.hexdigest()


def print_equal(dir):
    files = read_filepaths(dir)
    global dict
    for file in files:
        h = get_hash(file)
        if dict.get(h) == None:
            dict[h] = []
        dict[h].append(file)
    for lst in dict.values():
        if len(lst) > 1:
            print(':'.join(lst))


def main():
    if len(sys.argv) != 2:
        print("usage: ./solution.py dir")
        sys.exit(1)
    dir = sys.argv[1]
    print_equal(dir)

if __name__ == '__main__':
    main()