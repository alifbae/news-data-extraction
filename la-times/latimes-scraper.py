#!/usr/bin/env python
""" 
Takes a list of URLS or a URL from the latimes 
and appends the data to a JSON file
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
		if "www.seattletimes.com" in self.url:
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
		'div', {'class': 'trb_article_page'})))

		contentFilter = (BeautifulSoup(str(
			contentSoup.find_all('p'))).get_text()).encode('ascii',errors='ignore')

		clean1 = contentFilter.replace("\n", '')
		clean2 = clean1.replace('[, , ', '')
		clean3 = clean2.replace("., ", ". ")
		clean4 = clean3.replace(". , ", ". ")
		clean5 = clean4.encode('string-escape').replace("\\'", '')
		clean6 = clean5.replace('[, ', '[')
		clean7 = clean6.replace('[[', '[')
		return clean7

	def titleFilter(self, pageSoup):
		return BeautifulSoup(str(pageSoup.find_all(
			'h1', {'class': 'trb_article_title_text'}))).get_text().encode('ascii',errors='ignore')

	def authorFilter(self, pageSoup):
		return BeautifulSoup(str(pageSoup.find_all(
			'a', {'class': 'trb_bylines_name_author_a'}))).get_text().encode('ascii',errors='ignore')

	def dateFilter(self, pageSoup):
		dateFilter = pageSoup.find_all('time', {"datetime":True})
		for date in dateFilter:
			dateLineString = date['datetime'][:10] #remove time from datetime

		dateLineFormated = str(datetime.datetime.strptime(
			dateLineString, "%Y-%m-%d").date()).replace('-','')

		return dateLineFormated

	def dumpToJsonFile(self, content, filename, filemode):
		with open(filename, filemode) as f:
			f.write(json.dumps(content)+'\n')

def main():
	test = Crawler("http://www.latimes.com/nation/politics/la-na-latino-voters-20150910-story.html")
	testBuffer = test.getHtmlBuffer()
	testData = test.extractContentFromHtml(testBuffer)
	print testData
	test.dumpToJsonFile(testData, 'testDump.json', 'a+')


main()
