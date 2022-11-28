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
    isDirector = soup.isDirector.text
    isOfficer = soup.isOfficer.text
    isOther = soup.isOther.text
    if isOfficer == "1":
        officerTitle = soup.officerTitle.text
    

    print(date+name+ticker+isDirector+isOfficer+isOther+officerTitle)

readData("https://www.sec.gov//Archives/edgar/data/1463172/000146317222000368/wf-form4_166942720012433.xml")