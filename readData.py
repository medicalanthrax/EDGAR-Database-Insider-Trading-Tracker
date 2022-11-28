from bs4 import BeautifulSoup
import requests

def readData(URL):
    headers = {
        "User-Agent" : "Carlo Tran carlotran4@gmail.com"
    }
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content,"xml")

    date = soup.periodOfReport.text
    name = soup.issuerName.text
    ticker = soup.issuerTradingSymbol.text
    if(soup.isDirector) != None:
        isDirector = soup.isDirector.text
    else: isDirector = "0"
    if(soup.isOfficer) != None:
        isOfficer = soup.isOfficer.text
    else: isOfficer = "0"
    isOther = soup.isOther.text
    if isOfficer == "1":
        officerTitle = soup.officerTitle.text
    else: officerTitle = ""
    
    
    print(date+name+ticker+isDirector+isOfficer+isOther+officerTitle)

