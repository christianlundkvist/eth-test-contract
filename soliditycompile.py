import subprocess as sp
import re

def compile(filename):
    output = sp.check_output(['solc', '--binary', 'stdout', filename])
    m = re.search('([a-f0-9]+)$', output)
    return m.group(1).decode('hex')

if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    print compile(filename).encode('hex')
