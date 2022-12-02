"""Contains collect_links"""
import re
import requests
from bs4 import BeautifulSoup


def collect_links():
    """ Collect all the EDGAR links that have not yet been parsed

    Returns list of links to xml files
    """
    url = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=4&owner=only&count=100&action=getcurrent"
    headers = {
        "User-Agent": "Carlo Tran carlotran4@gmail.com"
    }
    page = requests.get(url, headers=headers, timeout=30)

    soup = BeautifulSoup(page.content, "html.parser")

    # Get all Acc No's
    acc_no = []
    for i in soup.find_all(string=re.compile("Accession Number:")):
        i = i.replace("Accession Number: ", "")
        i = i.split()[0]
        acc_no.append(i)

    cik = []
    # Get all CIK's
    for i in soup.find_all("a"):
        i = str(i)
        if "cgi-bin" in i and "file" not in i and "getcurrent" not in i:
            cik.append(i[57:67])
    print(cik, acc_no, sep="\n")


collect_links()
