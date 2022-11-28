from collectLinks import collectLinks
from getDoc import getDoc
from readData import readData

links = collectLinks()
i=0
for link in links:
    print(link)
    readData(getDoc(link))
    i+=1
    print(i)