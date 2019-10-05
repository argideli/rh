import os
import re
import sys
import linecache
import argparse


class colorCodes:
    RED = '\x1b[1;31;40m'
    END = '\x1b[0m'

class regSearch:
    def __init__(self):
        #global args
        parser = argparse.ArgumentParser(description='Python grep implementation')
        parser.add_argument("-u", "--underscore", help="Print '^' under the matching text",
                            action="store_true")
        parser.add_argument("-c", "--color", help="Colorize output",
                            action="store_true")
        parser.add_argument("-m", "--machine", help="Generate machine readable output",
                            action="store_true")
        parser.add_argument('file',type=argparse.FileType('r'),nargs='?', default=sys.stdin) # TODO:  encoding='ascii'
        parser.add_argument('regex',type=argparse.FileType('r'),nargs='*', default=sys.stdin) # TODO:  encoding='ascii'
        #parser.add_argument('-f', '--file', nargs='+', type=argparse.FileType('r'), help='specify one or more input files')
        self.args = parser.parse_args()
        for arg in vars(self.args):
             print arg, getattr(self.args, arg)
        exit(0)

    def underscore(self,filename ,line,line_num,matches,search_str):
        """Inserts the underscore ^ character under every character that matches"""
        out = '{} line {}: '.format(filename,line_num)
        offset = len(out)
        out = out +'{}\n'.format(line)
        m_pos=[range(a,b) for a,b in zip(matches['start'],matches['stop'])]
        flatten = lambda l: [i+offset for subl in l for i in subl]
        for c in range(len(line)+offset):
            if c in flatten(m_pos):
                out += '^'
            else:
                out += ' '
        return out


    def colorize(self, filename, line,line_num,to_colr):
        out = '{} line {}: '.format(filename, line_num)
        if self.args.underscore == True:
            out = ''
        parts = line.split('{}'.format(to_colr))
        for part in parts[:-1]:
            out += part + colorCodes.RED + '{}'.format(to_colr) + colorCodes.END
        return out

    def machine(self, filename, line_num,matches,search_str):
        out = ''
        for match in matches['start']:
            out += '{}:{}:{}:{}\n'.format(filename,line_num,match,search_str)
        out = out.rstrip()
        return out

    def get_line(self, infile, line_num):
        line = linecache.getline(infile.name, line_num)
        line = line.rstrip()
        return line

    def match_lines(self, search_str, infile):
        line_num = 0
        exp = re.compile('.*({}).*'.format(search_str))
        for line in infile:
            line_num += 1
            line = line.rstrip()
            if re.search(exp, line):
                yield line_num

    def match_indices(self, search_str, infile):
        matches = {m: None for m in self.match_lines(search_str, infile)}
        for match in matches.keys():
            line = self.get_line(infile, match)
            starts = []
            stops = []
            for occ in re.finditer(search_str, line):
                starts.append(occ.start(0))
                stops.append(occ.end(0))
            matches[match] = {'start': starts,'stop': stops}
        return matches

    def output(self, infile, search_str):
        res = ''
        matches = self.match_indices(search_str, infile)
        for line_num in matches.keys():
            line = self.get_line(infile, line_num)
            start_pos = matches[line_num]['start']
            end_pos = matches[line_num]['stop']
            if self.args.machine == True:
                res = self.machine(infile.name, line_num, matches[line_num], search_str)
            elif self.args.underscore == True:
                res = self.underscore(infile.name, line, line_num, matches[line_num], search_str)
                if self.args.color == True:
                    res = self.colorize(infile.name, res, line_num, len(search_str) * '^')
            elif self.args.color == True:
                res = self.colorize(infile.name,line, line_num, search_str)


            print res




print '###########################################################'
finder = regSearch()
search_str = 'kwin'
filename = 'file1.txt'
for file in finder.args.file:
    finder.output(file, search_str)
