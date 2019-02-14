import sys
import json
filename = sys.argv[1]

def format(data):
    dic = {}
    for k in data:
        if isinstance(data[k], dict):
            for child_k in data[k]:
                dic["%s_%s" % (k, child_k)] = data[k][child_k]
        else:
            dic[k] = data[k]
    return dic

def existdict(data):
    for k in data.keys():
        if isinstance(line[k], dict):
            return True
    return False

F=open(filename, 'r')
title = []
while True:
    lines = F.readline().strip('\n')
    if lines:
        line = json.loads(lines)
        while True:
            if existdict(line):
                line = format(line)
            else:
                break
        if not title:
            title = [j for j in line]
            print('\t'.join(title))
        finally_data = {}
        for t in title:
            try:
                finally_data[t] = line[t]
            except:
                finally_data[t] = 'null'

        print('\t'.join([str(finally_data[j]) for j in title]))
    else:
        break