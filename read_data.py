"""Contains read_data method"""

from bs4 import BeautifulSoup
import requests
from text import text

def read_data(url):
    """ Given a url to a form 4 xml sheet, return a list of the relevant information

    Example Usage:
        print(read_data("example_url.com"))
        my_data = read_data("example_url.com")

    """
    page = requests.get(url,headers={"User-Agent" : "Carlo Tran carlotran4@gmail.com"},timeout=30)

    soup = BeautifulSoup(page.content,"xml")

    date = soup.periodOfReport.text
    name = soup.issuerName.text
    ticker = soup.issuerTradingSymbol.text

    #Prevent NoneType errors due to inconsistent existence of title variables.
    if(soup.isDirector) is not None:
        is_director = soup.isDirector.text
    else: is_director = "0"
    if(soup.isOfficer) is not None:
        is_officer = soup.isOfficer.text
    else: is_officer = "0"
    if soup.isOther is not None :
        is_other = soup.isOther.text
    else: is_other = "0"
    if is_officer == "1":
        officer_title = soup.officerTitle.text
    else: officer_title = ""

    title = ""
    if is_director == "1":
        title+="Director,"
    if is_officer =="1" and len(officer_title)>0:
        title+=officer_title+","
    elif is_officer =="1":
        title+="Officer,"
    if is_other == "1":
        title+= "Other"


    derivative_transactions = soup.find_all("derivativeTransaction")
    non_derivative_transactions = soup.find_all("nonDerivativeTransaction")

    transactions = []
    for i in derivative_transactions:
        transactions.append([
            text(i.securityTitle.value),
            text(i.transactionCode),
            text(i.transactionPricePerShare.value),
            text(i.transactionShares.value)
        ])
    for i in non_derivative_transactions:
        transactions.append([
            text(i.securityTitle.value),
            text(i.transactionCode),
            text(i.transactionPricePerShare.value),
            text(i.transactionShares.value)
        ])

    return ([date,name,ticker,title,transactions])
