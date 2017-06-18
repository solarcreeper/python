import re

file = open('txt.txt', 'r').read()

pattren = re.compile('.*?self.addParameters(.*?)\)', re.S)
result = re.findall(pattren, file)
pass
