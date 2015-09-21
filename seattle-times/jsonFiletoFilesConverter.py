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
			with open("seattletimes-jsondata.json", 'a+') as g:
				g.write(json.dumps(articleData)+'\n')

def makeJsonFiles():
	articleData = []
	with open("seattletimes-jsondata.json") as f:
		for line in f:
			articleData.append(json.loads(line))

	articleCounter = 0
	for data in articleData:
		with open(("articleData2/seattletimes-article-"+str(articleCounter)+".json"), 'w+') as g:
			g.write(json.dumps(data))
		articleCounter += 1

makeJsonFiles()