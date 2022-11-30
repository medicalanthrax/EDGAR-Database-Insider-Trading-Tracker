from collectLinks import collectLinks
from getDoc import getDoc
from readData import readData

links = collectLinks()
for link in links:
    print(link)
    print(readData(getDoc(link)))