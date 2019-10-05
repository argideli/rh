import os
import re
import sys
import linecache
import argparse


class strFind:
    def __init__(self):
        pass

    def __underscore__():
        pass

    def __colorize__():
        pass

    def __machine__():
        pass

    def get_line(self, filename, line_num):
        line = linecache.getline(filename, line_num)
        line = line.rstrip()
        return line

    def match_lines(self, search_str, infile):
        exp = re.compile('.*({}).*'.format(search_str))
        line_num = 0
        for line in infile:
            line_num += 1
            line = line.rstrip()
            if re.search(exp, line):
                yield line_num

    def match_indices(self, search_str, filename):
        matches = {m: None for m in match_lines(search_str, infile)}
        for match in matches.keys():
            line = get_line(filename, match)
            matches[match] = [(occ.start(0), occ.end(0)) for occ in re.finditer(search_str, line)]
        return matches

    def output(self, filename, matches):
        for m in matches.keys():
            #print matches[m]
            print finder.get_line(filename, m)


finder = strFind()
matches = []
search_str = 'jedi'
filename = 'file.txt'
with open(filename, "r") as infile:
    #print finder.match_lines(search_str, infile)
    matches = finder.match_indices(search_str, filename)
    #for match in match_lines(search_str, infile):
    #    matches.append(match)



#print matches
#print finder.match_indices(search_str, matches, filename)
print matches
