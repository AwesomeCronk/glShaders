import sys

fileIn = open(sys.argv[1], 'r')
fileOut = open(sys.argv[2], 'w')

dataIn = fileIn.read()
for c in dataIn:
    if c == '\t':
        cOut = '    '
    else:
       cOut = c
    fileOut.write(cOut)
fileIn.close()
fileOut.close()