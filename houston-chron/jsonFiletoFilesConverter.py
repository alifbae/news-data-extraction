#!/usr/bin/env python

import json
import os



def makeSingleJson():
	dirPath = "articleData/"
	paths = os.listdir(dirPath)

	for filePath in paths:
		print "articleData2/"+filePath
		with open(dirPath+filePath) as f:
			articleData = json.load(f)
			with open("latimes-data-all.json", 'a+') as g:
				g.write(json.dumps(articleData)+'\n')
	return

def makeJsonFiles():
	articleData = []
	articleCounter = 0

	with open("houstonChron-data-all-v3.json") as f:
		for line in f:
			articleData.append(json.loads(line))

	for data in articleData:
		with open(("articleData-houston-chron/chicago-tribune-article-"+str(articleCounter)+".json"), 'w+') as g:
			g.write(json.dumps(data))
		articleCounter += 1
	return

# makeSingleJson()
makeJsonFiles()