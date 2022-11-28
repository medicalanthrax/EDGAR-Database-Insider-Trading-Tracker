from bs4 import BeautifulSoup
import requests 

def getData(URL):
    headers = {
        "User-Agent" : "Carlo Tran carlotran4@gmail.com"
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content,"html.parser")

    links = []
    goodLinks = []
    for i in soup.find_all("a"):
        links.append(i.get("href"))

    for link in links:
        if link.__contains__("Archives/edgar/data") and link.__contains__("xml") and not(link.__contains__("xsl")):
            goodLinks.append("https://www.sec.gov/"+link)
    if len(goodLinks)>0:
        return goodLinks[0]

