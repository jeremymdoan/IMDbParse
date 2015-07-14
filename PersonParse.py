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
            elif count == 100:
                break
            else:
                yield line
                count += 1

def extractPersonData(line):
    pat = re.compile(r'^([^\t]*)\t+(.*)\s\((\d+)?\/?I*\)\s(.*)$')
    g = pat.match(line)
    output = [g.group(1), g.group(2), g.group(3)]
    pat2 = ('(^\{.*\})', '(\[.*\])','(\(T?V\))', '\((archive\sfootage|voice)\)')
    for p in pat2:
        g2 = re.search(p, g.group(4))
        thing = g2.group(1) if g2 else ''
        output.append(thing)
    return '~'.join(output)

tuples = list(extractPersonData(line) for line in readPersonLines('actors.list'))
for t in tuples:
    print(t)
