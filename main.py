#!/usr/bin/python3
import re
import sys

def getChangeDict(changeList):
	changeDict = {}
	for flpath, lineno, textln in changeList:
		if flpath not in changeDict:
			changeDict[flpath] = {}
		changeDict[flpath][lineno] = textln
	return changeDict

def readLines(flpath):
	with open(flpath) as f:
		lines = f.readlines()
	return lines

def writeLines(flpath, lines):
	with open(flpath, 'w') as f:
		for item in lines:
			f.write('%s' % item)

def appliesFile(flpath, change):
	lines = readLines(flpath)
	for lineno in change:
		lines[lineno] = change[lineno]
	writeLines(flpath, lines)

def applies(changeList):
	changeDict = getChangeDict(changeList)
	for flpath in changeDict:
		appliesFile(flpath, changeDict[flpath])

def process(f):
	changeList = []
	for line in f:
		if not line.strip():
			continue
		m = re.search('[:-]\d+[:-]', line)
		if m:
			s, t = m.span()
			flpath = line[:s]
			lineno = int(line[s+1:t-1])-1
			textln = line[t:]
			changeList.append((flpath, lineno, textln))
		else:
			raise Exception('Invalid format: "%s"' % repr(line))
		
	applies(changeList)


if len(sys.argv) != 2:
	print('''
	edit-after-git-grep
	
	1. git grep -n YOUR_PATTERN > /tmp/a.txt
	2. Edit /tmp/a.txt
	3. python3 main.py /tmp/a.txt
	''')
	
else:
	if sys.argv[1] == '-':
		process(sys.stdin)
	else:
		with open(sys.argv[1]) as f:
			process(f)
