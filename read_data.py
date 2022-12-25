"""Contains read_data method"""

import time

import requests
from bs4 import BeautifulSoup
from text import text
from ratelimiter import RateLimiter

@RateLimiter(max_calls=5,period=1)
def read_data(url):
    """ Given a url to a form 4 xml sheet, return a list of the relevant information

    Returns:[Date, Name, Ticker, Title,
            Security Titles(sep=\\n), Transaction Code(sep=\\n),
            No. Shares(sep=\\n), Price Per Share(sep=\\n)]
    Please note that multiple transactions may be listed, hence the list of transaction lists.

    """
    try:
        page = requests.get(
            url, headers={"User-Agent": "Carlo Tran carlotran4@gmail.com"}, timeout=120)

        soup = BeautifulSoup(page.content, "xml")

        date = soup.periodOfReport.text
        name = soup.issuerName.text
        ticker = soup.issuerTradingSymbol.text

        titles = ""

        for i in soup.find_all("reportingOwner"):
        # Prevent NoneType errors due to inconsistent existence of title variables.
            is_director = "0"
            if (i.isDirector) is not None:
                is_director = i.isDirector.text
            is_officer = "0"
            if (i.isOfficer) is not None:
                is_officer = i.isOfficer.text
            is_other = "0"
            if i.isOther is not None:
                is_other = i.isOther.text
            officer_title = ""
            if is_officer == "1":
                officer_title = i.officerTitle.text
            is_ten_percent_owner = "0"
            if (i.isTenPercentOwner) is not None:
                is_ten_percent_owner = i.isTenPercentOwner.text

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
            titles = titles+title+"\n"
        titles = titles[0:-1]
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
            if(i.transactionShares) is not None:
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
                f"{name} ({ticker})",
                f"\"{titles}\"",
                f"\"{security_title}\"",
                f"\"{transaction_code}\"",
                f"\"{transaction_shares}\"",
                f"\"{transaction_price_per_share}\""
                ])
    except:           #pylint: disable = bare-except
        print(f"error at {url}")
        time.sleep(630)
        return []
