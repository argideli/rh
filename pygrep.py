import os
import re
import sys
import argparse
import tempfile
import linecache

class colorCodes:
    RED = '\x1b[1;31;40m'
    END = '\x1b[0m'


class regSearch:
    def __init__(self):
        """Constructor, initializes the argument parser (argparse) and runs checks on the provided arguments."""
        parser = argparse.ArgumentParser(
            description='Python grep implementation')
        parser.add_argument(
            "-u",
            "--underscore",
            help="Print '^' under the matching text",
            action="store_true")
        parser.add_argument("-c", "--color", help="Colorize matches",
                            action="store_true")
        parser.add_argument(
            "-m",
            "--machine",
            help="Generate machine readable output",
            action="store_true")
        parser.add_argument(
            'regex',
            nargs=1,
            action="store",
            help="Search expresion enclosed in single quotes ex. 'something.*[0-9]'")
        parser.add_argument(
            'files',
            type=argparse.FileType('r'),
            nargs='*',
            default=sys.stdin,
            help="One or two files to be searched for matches of [regex]")
        self.args = parser.parse_args()
        self.exp = re.compile('.*({}).*'.format(self.args.regex[0]))
        for arg in vars(self.args):
            print(arg, getattr(self.args, arg), type(getattr(self.args, arg)))
        if not (self.args.underscore or self.args.machine or self.args.color):
            parser.error('Please select the output format [-c, -u, -uc, -m]')
        if self.args.machine and (self.args.underscore or self.args.color):
            parser.error('Machine format [-m] cannot be  combined with [-c] or [-u]')
        if len(self.args.regex[0]) == 0 or self.args.regex[0].isspace():
            parser.error('Invalid expression') #Error if regex empty or not set
        if sys.stdin.isatty() and self.args.files is sys.stdin: #Error if no file specified on tty
            parser.error('No input file specified')
        try:
            if len(self.args.files) not in (1, 2):
                parser.error('Input files limit of 2 exceeded') #Error if files are more than two
        except TypeError:
            pass

    def underscore(self, filename, line, line_num, matches):
        """Inserts the underscore ^ character under every character position (whiteline until then), the start and end position of the match are provided by the [matches] dictionary, the resulting string containing two lines is returned.
        """
        out = '{} line {}: '.format(filename, line_num)
        offset = len(out)
        out = out + '{}\n'.format(line)
        m_pos = [range(a, b) for a, b in zip( matches['start'], matches['stop'])]

        def flatten(l): return [i + offset for subl in l for i in subl] #Flatten a list of lists
        for c in range(len(line) + offset):
            if c in flatten(m_pos):
                out += '^'
            else:
                out += ' '
        return out

    def colorize(self, filename, line, line_num, to_colr):
        """Returns the input [line] with the matches colorized by partitioning on the matched string [to_colr] and inserting the color codes in the appropriate position.
        """
        out = '{} line {}: '.format(filename, line_num)
        if self.args.underscore:
            out = ''
        parts = line.split('{}'.format(to_colr))
        for part in parts[:-1]:
            out += part + colorCodes.RED + '{}'.format(to_colr) + colorCodes.END
        out += parts[-1]
        return out

    def machine(self, filename, line_num, matches, matched):
        """Prints out the matches found in every line in machine understood file_name:no_line:start_pos:matched_text ."""
        out = ''
        out += '{}:{}:{}:{}\n'.format(filename, line_num, matches['start'][0], matched) # Comment line to allow overlap
        #for match in matches['start']: #Comment out to allow overlap
        #    out += '{}:{}:{}:{}\n'.format(filename, line_num, match+1, matched) #Comment out to allow overlap
        out = out.rstrip()
        return out

    def get_line(self, infile, line_num):
        """Read the line with line number [line_num] from [infile] and return her."""
        line = linecache.getline(infile.name, line_num)
        line = line.rstrip()
        return line

    def match_lines(self, infile):
        """Generator function used in function match_indices to initialize the matches dictionary"""
        line_num = 0
        for line in infile:
            line_num += 1
            line = line.rstrip()
            if re.search(self.exp, line):
                yield line_num

    def match_indices(self, infile):
        """Initializes a dictionary with keys the lines that matched the regular expresion provided, then inserts a sub-dictionary for evrey key that contains the list of positions that matches start and end ex. line: {'start': [start1, start2], 'stop': [stop1, stop2]}"""
        matches = {m: None for m in self.match_lines(infile)}
        for match in matches.keys():
            line = self.get_line(infile, match)
            starts = []
            stops = []
            for occ in re.finditer('(?=({}))'.format(self.args.regex[0]), line): #Ensure repetition with ?= and provide the uncompiled regex from the argument
                starts.append(occ.start(1))
                stops.append(occ.end(1))
            matches[match] = {'start': starts, 'stop': stops}
        return matches

    def output(self, infile):
        """Gets the index for every match, reads the line containing the match from [infile] and calls the appropriate function to format the output as specified by the user and prints it."""
        res = ''
        matches = self.match_indices(infile)
        for line_num in sorted(matches.keys()):
            line = self.get_line(infile, line_num)
            matched_string = self.exp.match(line).group(1)
            start_pos = matches[line_num]['start']
            end_pos = matches[line_num]['stop']
            if self.args.machine:
                res = self.machine(
                    infile.name,
                    line_num,
                    matches[line_num],
                    matched_string)
            elif self.args.underscore:
                res = self.underscore(
                    infile.name, line, line_num, matches[line_num])
                if self.args.color:
                    res = self.colorize(
                        infile.name, res, line_num, len(matched_string) * '^')
            elif self.args.color:
                res = self.colorize(
                    infile.name, line, line_num, matched_string)
            print(res) # Python 3 compatibility


if __name__ == '__main__':
    finder = regSearch()
    if sys.stdin.isatty():
        for file in finder.args.files:
            finder.output(file)
            file.close()  # Close the files handle, because argparse leaves them open
    else:
        temp = tempfile.NamedTemporaryFile('r+w') #,encoding=ascii' Use tempfile to bypass limitation of re module not being able to use regexes on a stream. Alternatively the regex mdule can be used
        try:
            temp.writelines('{}'.format(sys.stdin.read()))
            temp.seek(0)
            finder.output(temp)
        finally:
            temp.close()
