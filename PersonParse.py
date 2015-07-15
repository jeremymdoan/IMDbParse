__author__ = 'jeremy.doan'

import re
from uuid import uuid4
import os

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
            #elif count == 1000:
            #    break
            else:
                yield line
                count += 1

def extractPersonData(line):
    pat = re.compile(r'^([^\t]*)\t+(.*)\s\((\d{4})\S*\)\s(.*)$')
    g = pat.match(line)
    global name
    try:
        name = getName(g.group(1)) if not g.group(1) == '' else name
    except AttributeError:
        return '!&8%$#' + line
    output = [name, g.group(2), g.group(3)]
    pat2 = ('(^\{.*\})', '(\[.*\])','(\(T?V\))', '\((archive\sfootage|voice)\)')
    for p in pat2:
        g2 = re.search(p, g.group(4))
        thing = g2.group(1) if g2 else ''
        output.append(thing)
    try:
        return re.sub("[\[\]\{\}]", "", '~'.join(output))
    except TypeError:
        return '!&8%$#' + line

def getName(name):
    g = re.search('(^.*),\s(.*)', name)
    name = g.group(2) + " " + g.group(1) if g else name
    g = re.search('(^.*)\s(\(\w*)\s(.*$)', name)
    name = g.group(1) + " " + g.group(3) + " " + g.group(2) if g else name
    return str(uuid4()).replace("-", "")[:8] + "~" + name

def run(filename):
    lines = (extractPersonData(line) for line in readPersonLines(filename))
    output_file = os.path.splitext(os.path.basename(filename))[0] + '.txt'
    for f in [output_file, 'error_lines.txt']:
        if os.path.exists(f):
            os.remove(f)
    with open(output_file, 'w') as out_file:
        with open('error_lines.txt', 'w') as error_file:
            counter = 0
            for line in lines:
                if  line[:6] == '!&8%$#':
                    error_file.write(line + '\n')
                else:
                    out_file.write(line + '\n')
                counter += 1
                """if counter%10000 == 0:
                    print("flushing")
                    out_file.flush()
                    error_file.flush()"""

if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run('actors.list')
