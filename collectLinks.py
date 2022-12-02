import requests
from bs4 import BeautifulSoup
def collectLinks():
    URL = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=4&owner=only&count=100&action=getcurrent"
    headers = {
        "User-Agent" : "Carlo Tran carlotran4@gmail.com"
    }
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content,"html.parser")

    links = []
    goodLinks = []
    for link in soup.find_all("a"):
        links.append(link.get("href"))

    for link in links:
        if (link.__contains__("cgi-bin") 
        and not link.__contains__("file") 
        and not link.__contains__("getcurrent")):
            goodLinks.append("https://www.sec.gov/"+link)

    return goodLinks
