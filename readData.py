from bs4 import BeautifulSoup
import requests
from text import text

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
	
	derivativeTransactions = soup.find_all("derivativeTransaction")
	nonDerivativeTransactions = soup.find_all("nonDerivativeTransaction")

	transactions = []
	for i in derivativeTransactions:
		transactions.append([
			text(i.securityTitle.value),
			text(i.transactionCode),
			text(i.transactionPricePerShare.value),
			text(i.transactionShares.value)
		])
	for i in nonDerivativeTransactions:
		transactions.append([
			text(i.securityTitle.value), 
			text(i.transactionCode), 
			text(i.transactionPricePerShare.value),
			text(i.transactionShares.value)
		])
		
	transactions.append([name])
	return (transactions)

#print(readData("https://www.sec.gov/Archives/edgar/data/764897/000106299322022843/form4.xml"))
#print(readData("https://www.sec.gov/Archives/edgar/data/919567/000120709722000460/primary_doc.xml"))