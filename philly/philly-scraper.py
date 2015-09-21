#!/usr/bin/env python
""" 
Takes a list of URLS or a URL from the Philladelphia Inquirer 
and outputes a JSON array of objects
"""

import json
import urllib2
import httplib
import datetime
from bs4 import BeautifulSoup

__author__ = "Ali Fawad"

class Crawler():
	def __init__(self, Url):
		self.url = Url

	def validateURL(self):
		if "www.philly.com" in self.url:
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
		'div', {'class': 'body-content'})))

		contentFilter = (BeautifulSoup(str(contentSoup.find_all(
			'p'))).get_text()).encode('ascii',errors='ignore')

		filter1 = contentFilter.replace("\n", '')
		filter2 = filter1.replace('[, , ', '')
		filter3 = filter2.replace("., ", ". ")
		filter4 = filter3.replace(". , ", ". ")
		filter5 = filter4.encode('string-escape').replace("\\'", '')
		filter6 = filter5.replace('[, ', '[')
		filter7 = filter6.replace('[[', '[')
		filter8 = filter7.replace('[ , ', '[')
		filter9 = filter8.replace("\t", '')

		return filter9

	def titleFilter(self, pageSoup):
		return BeautifulSoup(str(pageSoup.find_all(
			'h1', {'class': 'entry-title'}))).get_text().encode('ascii',errors='ignore')

	def authorFilter(self, pageSoup):
		return BeautifulSoup(str(pageSoup.find_all(
			'h5', {'class': 'byline'}))).get_text().encode('ascii',errors='ignore')

	def dateFilter(self, pageSoup):
		dateSoup = BeautifulSoup(str(pageSoup.find_all('div', {'class': 'article_timestamp'})))
		dateString = BeautifulSoup(str(dateSoup.find_all('span'))).get_text().encode('ascii',errors='ignore')
		dateLine = str(datetime.datetime.strptime(dateString, "[%A, %B %d, %Y, %I:%M %p]").date()).replace('-', '')
		return dateLine

	def dumpToJsonFile(self, content, filename, filemode):
		with open(filename, filemode) as f:
			f.write(json.dumps(content)+'\n')

def main():
	test = Crawler("http://www.philly.com/philly/blogs/attytood/The-No-1-issue-for-the-presidential-race----in-2016.html")
	testBuffer = test.getHtmlBuffer()
	testData = test.extractContentFromHtml(testBuffer)
	test.dumpToJsonFile(testData, 'testDump.json', 'a+')


main()
