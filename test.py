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
        parser = argparse.ArgumentParser(description='Python grep implementation')
        parser.add_argument("-u", "--underscore", help="Print '^' under the matching text",
                            action="store_true")
        parser.add_argument("-c", "--color", help="Colorize output",
                            action="store_true")
        parser.add_argument("-m", "--machine", help="Generate machine readable output",
                            action="store_true")
        parser.add_argument('regex',nargs=1, action="store", help="Search expresion enclosed in single quotes ex. 'str.*[0-9]'") # TODO:  encoding='ascii'
        parser.add_argument('files',type=argparse.FileType('r'),nargs='*', default=sys.stdin, help="One or two files to be searched for matches of [regex]") # TODO:  encoding='ascii'
        self.args = parser.parse_args()
        self.exp = re.compile('.*({}).*'.format(self.args.regex[0]))
        print len(self.args.regex[0])
        print self.args.regex[0].isspace()
        if len(self.args.regex[0]) == 0 or self.args.regex[0].isspace():
            parser.error('Invalid expression')

        for arg in vars(self.args):
             print arg, getattr(self.args, arg)

        try:
            if len(self.args.files) not in (1, 2):
                parser.error('Input files limit of 2 exceeded')
        except TypeError:
            pass

        exit(0)

    def underscore(self,filesname ,line,line_num,matches):
        """Inserts the underscore ^ character under every character that matches"""
        out = '{} line {}: '.format(filesname,line_num)
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


    def colorize(self, filesname, line,line_num,to_colr):
        out = '{} line {}: '.format(filesname, line_num)
        if self.args.underscore == True:
            out = ''
        parts = line.split('{}'.format(to_colr))
        for part in parts[:-1]:
            out += part + colorCodes.RED + '{}'.format(to_colr) + colorCodes.END
        return out

    def machine(self, filesname, line_num,matches,matched):
        out = ''
        for match in matches['start']:
            out += '{}:{}:{}:{}\n'.format(filesname,line_num,match,matched)
        out = out.rstrip()
        return out

    def get_line(self, infiles, line_num):
        line = linecache.getline(infiles.name, line_num)
        line = line.rstrip()
        return line

    def match_lines(self,infiles):
        line_num = 0
        for line in infiles:
            line_num += 1
            line = line.rstrip()
            if re.search(self.exp, line):
                yield line_num

    def match_indices(self,infiles):
        matches = {m: None for m in self.match_lines(infiles)}
        for match in matches.keys():
            line = self.get_line(infiles, match)
            starts = []
            stops = []
            for occ in re.finditer(self.exp, line):
                starts.append(occ.start(0))
                stops.append(occ.end(0))
            matches[match] = {'start': starts,'stop': stops}
        return matches

    def output(self, infiles):
        res = ''
        matches = self.match_indices(infiles)
        for line_num in sorted(matches.keys()):
            line = self.get_line(infiles, line_num)
            matched_string = self.exp.match(line).group(1)
            start_pos = matches[line_num]['start']
            end_pos = matches[line_num]['stop']
            if self.args.machine == True:
                res = self.machine(infiles.name, line_num, matches[line_num], matched_string)
            elif self.args.underscore == True:
                res = self.underscore(infiles.name, line, line_num, matches[line_num])
                if self.args.color == True:
                    res = self.colorize(infiles.name, res, line_num, len(matched_string) * '^')
            elif self.args.color == True:
                res = self.colorize(infiles.name,line, line_num, matched_string)
            print res




print '###########################################################'
finder = regSearch()
for files in finder.args.files:
    finder.output(files)
    files.close() #Close the files handler because argparse leaves them open
