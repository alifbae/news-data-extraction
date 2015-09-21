#!/usr/bin/env python
""" 
Takes a list of URLS or a URL from the Seattle times
and appends the data to a JSON file
"""

import json
import urllib2
import httplib
import datetime
from bs4 import BeautifulSoup

__author__ = "Ali Fawad"

class SeattleTimesCrawler():
	def __init__(self, Url):
		self.url = Url

	def validateURL(self):
		if "www.latimes.com" in self.url:
			return True
		else:
			return False

	def getHtmlBuffer(self):
		try:
			htmlBuffer = urllib2.urlopen(self.url).read()
			return htmlBuffer
		except urllib2.HTTPError, err:
			print "HTTP Error: " + str(err)
			return -1
		except httplib.IncompleteRead, err:
			print "Incomplete Read Error: " + str(err)
			return -1

	def extractContentFromHtml(self, htmlBuffer):
		if htmlBuffer == -1:
			return -1

		else:		
			articleInfo = {}
			pageSoup = BeautifulSoup(htmlBuffer)
			articleInfo['Link'] = self.url
			articleInfo['Author'] = self.authorFilter(pageSoup)
			articleInfo['Title'] = self.titleFilter(pageSoup)
			articleInfo['Content'] = self.contentFilter(pageSoup)
			articleInfo['Date'] = self.dateFilter(pageSoup)
			return articleInfo

	def contentFilter(self, pageSoup):
		contentSoup = BeautifulSoup(str(pageSoup.find_all(
			'div', {'class': 'main-story-content entry-content'})))

		contentFilter = (BeautifulSoup(str(
			contentSoup.find_all('p'))).get_text()).encode('ascii',errors='ignore')

		filter1 = contentFilter.replace("\n", '')
		filter2 = filter1.replace('[, , ', '')
		filter3 = filter2.replace("., ", ". ")
		filter4 = filter3.replace(". , ", ". ")
		filter5 = filter4.encode('string-escape').replace("\\'", '')
		filter6 = filter5.replace('[, ', '[')
		filter7 = filter6.replace('[[', '[')
		filter8 = filter7.replace("\t", '')

		if '___' in filter8: #if true, get content till start of footer
			stringEnd = filter8.find("___")
			return filter8[:stringEnd]
		else:
			return filter8

	def titleFilter(self, pageSoup):
		title = BeautifulSoup(str(pageSoup.find_all(
			'h1', {'class': 'article-title p-name entry-title'}))).get_text().encode(
			'ascii',errors='ignore')
		title = title.replace("\n", "")
		title = title.replace("      ", "")
		return title

	def authorFilter(self, pageSoup):
		author = BeautifulSoup(str(pageSoup.find_all(
			'a', {'class': 'p-author h-card hcard url fn'}))).get_text().encode('ascii',errors='ignore')
		author = author.replace("\n", '')
		return author

	def dateFilter(self, pageSoup):
		dateFilter = pageSoup.find_all('time', {"datetime":True})
		for date in dateFilter:
			dateLineString = date['datetime']
			break #only get published date, not updated date

		dateLineFormated = str(datetime.datetime.strptime(
			dateLineString, "%Y-%m-%d %H:%M:%S").date()).replace('-','')

		return dateLineFormated

	def dumpToJsonFile(self, content, filename, filemode):
		with open(filename, filemode) as f:
			f.write(json.dumps(content)+'\n')

def main():
	test = SeattleTimesCrawler("http://www.seattletimes.com/seattle-news/transportation/qa-a-guide-to-using-i-405s-new-express-toll-lanes/")
	testBuffer = test.getHtmlBuffer()
	testData = test.extractContentFromHtml(testBuffer)
	print testData
	test.dumpToJsonFile(testData, 'testDump.json', 'a+')


main()
