import requests
from bs4 import BeautifulSoup
from getData import getData
def getDoc(URL):
    headers = {
        "User-Agent" : "Carlo Tran carlotran4@gmail.com"
    }
    page = requests.get(URL, headers=headers,timeout=30)
    soup = BeautifulSoup(page.content,"html.parser")
    if len(soup.find_all(id= "documentsbutton"))>0:
        link = soup.find_all(id= "documentsbutton")[0].get("href")
    else: return ""
    return getData ("https://www.sec.gov/"+link)
