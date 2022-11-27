from collectLinks import collectLinks
from getDoc import getDoc
from getData import getData

links = collectLinks()
i=0
for link in links:
    print(getDoc(link))
    i+=1
    print(i)