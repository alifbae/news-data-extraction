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


### How to use the data:
```python
import json
import os

articleDataDirectoryPath = "" #Whatever the path of the articleData directory is
filePathList = os.listDir(articleDataDirectoryPath) # will provide a list of filePaths

for filePath in filePathList:
	absFilePath = articleDataDirectoryPath + filePath
	with open(absFilePath) as f:
		for line in f:
			articleData = json.load(line) 

			#Do whatever with the data:
			title = articleData['Title']
			content = articleData['Content']
```


##### Currently data is available for:
- LA Times
- Seattle Times
- Houston Chronicle
- Chicago Tribune

##### Work in progress:
- Philly
