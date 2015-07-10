__author__ = 'jeremy.doan'

import re

def readPersonLines(filename):
    count = 0
    with open(filename) as file:
        line = file.readline()
        while not re.search(r'^Name.*', line):
            line = file.readline()
        file.readline()
        for line in file:
            if line == '\n' or re.search(r'^----.*', line):
                continue
            elif count == 50:
                break
            else:
                yield line
                count += 1

pat = re.compile(r'^([^\t]*)\t+(.*)\s\((\d+)?\/?I*\)\s(.*)$')
groups = (pat.match(line) for line in readPersonLines('actors.list'))
tuples = (g.groups() for g in groups if g)
for t in tuples:
    print(t)