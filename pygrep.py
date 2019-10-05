# /usr/bin/env python2
import re
import argparse


parser = argparse.ArgumentParser(description='Python grep implementation')

parser.add_argument("-u", "--underscore", help="Print '^' under the matching text",
                    action="store_true")
parser.add_argument("-c", "--color", help="Colorize output",
                    action="store_true")
parser.add_argument("-m", "--machine", help="Generate machine readable output",
                    action="store_true")
parser.add_argument('file', type=argparse.FileType('r'), nargs='*')
args = parser.parse_args()
print("Argument values:")
for arg in vars(args):
    print arg, getattr(args, arg)


thefile = open("test.txt", "r")
for line in thefile:
    line = line.strip()
    if re.match(r"cat", line):
        print(line)
exit(0)

pattern = re.compile("<(\d{4,5})>")


for i, line in enumerate(open('test.txt')):
    for match in re.finditer(pattern, line):
        print 'Found on line %s: %s' % (i+1, match.group())
