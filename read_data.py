"""Contains read_data method"""

from bs4 import BeautifulSoup
import requests
from text import text


def read_data(url):
    """ Given a url to a form 4 xml sheet, return a list of the relevant information

    Returns: [Date, Name, Ticker, Title, [[Security Title, Transaction Code, Price, No. Shares]]]
    Please note that multiple transactions may be listed, hence the list of transaction lists.

    """
    page = requests.get(
        url, headers={"User-Agent": "Carlo Tran carlotran4@gmail.com"}, timeout=30)

    soup = BeautifulSoup(page.content, "xml")

    date = soup.periodOfReport.text
    name = soup.issuerName.text
    ticker = soup.issuerTradingSymbol.text

    # Prevent NoneType errors due to inconsistent existence of title variables.
    if (soup.isDirector) is not None:
        is_director = soup.isDirector.text
    else:
        is_director = "0"
    if (soup.isOfficer) is not None:
        is_officer = soup.isOfficer.text
    else:
        is_officer = "0"
    if soup.isOther is not None:
        is_other = soup.isOther.text
    else:
        is_other = "0"
    if is_officer == "1":
        officer_title = soup.officerTitle.text
    else:
        officer_title = ""
    if (soup.isTenPercentOwner) is not None:
        is_ten_percent_owner = soup.isTenPercentOwner.text
    else:
        is_ten_percent_owner = "0"

    title = ""
    if is_director == "1":
        title += "Director,"
    if is_officer == "1" and len(officer_title) > 0:
        title += officer_title+","
    elif is_officer == "1":
        title += "Officer,"
    if is_ten_percent_owner == "1":
        title += "%10+ shareholder"
    if is_other == "1":
        title += "Other"
    # Remove hanging comma of title.
    if len(title) > 0 and title[len(title)-1] == ",":
        title = title[0:len(title)-1]

    derivative_transactions = soup.find_all("derivativeTransaction")
    non_derivative_transactions = soup.find_all("nonDerivativeTransaction")

    security_title = ""
    transaction_code = ""
    transaction_shares = ""
    transaction_price_per_share = ""
    for i in derivative_transactions:
        security_title = security_title+text(i.securityTitle.value)+"\n"
        transaction_code = transaction_code+text(i.transactionCode)+"\n"
        transaction_price_per_share = transaction_price_per_share + \
            text(i.transactionPricePerShare.value)+"\n"
        transaction_shares = transaction_shares + \
            text(i.transactionShares.value)+"\n"

    for i in non_derivative_transactions:
        security_title = security_title+text(i.securityTitle.value)+"\n"
        transaction_code = transaction_code+text(i.transactionCode)+"\n"
        transaction_price_per_share = transaction_price_per_share + \
            text(i.transactionPricePerShare.value)+"\n"
        transaction_shares = transaction_shares + \
            text(i.transactionShares.value)+"\n"

    if len(security_title)>0 and security_title[-1] == "\n":
        security_title = security_title[0:-1]
    if len(transaction_code)>0 and transaction_code[-1] == "\n":
        transaction_code = transaction_code[0:-1]
    if len(transaction_price_per_share)>0 and transaction_price_per_share[-1] == "\n":
        transaction_price_per_share = transaction_price_per_share[0:-1]
    if len(transaction_shares)>0 and transaction_shares[-1] == "\n":
        transaction_shares = transaction_shares[0:-1]
    return ([date,
            f"{name}({ticker})",
            f"{title}",
            f"\"{security_title}\"",
            f"\"{transaction_code}\"",
            f"\"{transaction_shares}\"",
            f"\"{transaction_price_per_share}\""
            ])
