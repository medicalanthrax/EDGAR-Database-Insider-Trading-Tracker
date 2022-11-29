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
    if soup.isOther != None :
        isOther = soup.isOther.text
    else: isOther = "0"
    if isOfficer == "1":
        officerTitle = soup.officerTitle.text
    else: officerTitle = ""

    footnote = soup.find_all("footnote")
    print(footnote)
    
    print(date+name+ticker+isDirector+isOfficer+isOther+officerTitle)

readData("https://www.sec.gov/Archives/edgar/data/764897/000106299322022843/form4.xml")