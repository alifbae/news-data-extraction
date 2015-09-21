#!/usr/bin/env python

import json
import os

dirPath = "articleData/"

paths = os.listdir(dirPath)

def makeSingleJson():
	for filePath in paths:
		print "articleData/"+filePath
		with open(dirPath+filePath) as f:
			articleData = json.load(f)
			with open("latimes-data-all.json", 'a+') as g:
				g.write(json.dumps(articleData)+'\n')
	return

def makeJsonFiles():
	articleData = []
	articleCounter = 0

	with open("latimes-data-all.json") as f:
		for line in f:
			articleData.append(json.loads(line))

	for data in articleData:
		with open(("articleData2/latimes-article-"+str(articleCounter)+".json"), 'w+') as g:
			g.write(json.dumps(data))
		articleCounter += 1
	return

# makeSingleJson()

makeJsonFiles()