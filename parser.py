#!/usr/bin/python
import sys
import re

DEFAULT_DIRECTORY = '/usr/g/service/log/scn.out'

def HelpText():
    print "\nEnter a regular expression, optionally followed by" + \
        " the path of a file you would like to search.\n" + \
        "    ./parser '[0-9a-f]+' /home/cni/parsing/parse.txt\n"
    exit()

if __name__ == "__main__":
    nargs = len(sys.argv)
    filename = DEFAULT_DIRECTORY
    if nargs == 1:
        HelpText()
    elif nargs > 2:
        filename = sys.argv[2]
    expr = sys.argv[1]
    f = open(filename, 'r')
    text = f.read()
    result = re.findall(expr, text, flags=re.DOTALL)
    if result:
        result = result[0]
        print result
        print "LENGTH OF RESULT: %d" % len(result)
    else:
        print 'Failed to match expression.'
