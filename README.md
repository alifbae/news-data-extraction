# News Data Extraction
### Scripts for extracting news articles from US newspapers

###### Scrapped data is available in folders inside the respective newspaper directory in the 'articleData' directory

#### Strucutre:
Each .json file in the articleData directory has one article data stored in valid json format. Each json array has 5 keys: 
- 'Title'   : Heading of the article
- 'Content' : Body of the article
- 'Date'    : Date the article was _published_
- 'Author'  : Author(s) of the article
- 'Link'    : URL of that article

<b>Note:</b> Some articles will have "NULL" in their 'Author' key, this is because those articles are op-eds or opinion pieces that 
don't necessarily have an author (eg: letters to the editor)

### How to use the data:
```python
import json
import os

articleDataDirectoryPath = "" # whatever the path of the articleData directory is
filePathList = os.listDir(articleDataDirectoryPath) # gets a list of filePaths

for filePath in filePathList:
	absFilePath = articleDataDirectoryPath + filePath
	with open(absFilePath) as f:
		for line in f:
			articleData = json.load(line) 

			# use the data:
			title = articleData['Title']
			content = articleData['Content']
			date = articleData['Date']
			url = articleData['Link']
			author = articleData['Author'] # use a check for "NULL" author if you wish
```

##### Currently data is available for:
- LA Times
- Seattle Times
- Houston Chronicle
- Chicago Tribune

##### Work in progress:
- Philly
