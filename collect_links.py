"""Contains collect_links"""
import requests
from bs4 import BeautifulSoup

def collect_links(directory):
    """Given a directory, find the link to the xml document.

    Parameter dir: https://www.sec.gov/Archives/edgar/data/CIK/Acc_No

    Returns: link of xml document.
    """

    headers = {
        "User-Agent": "Carlo Tran carlotran4@gmail.com"
    }
    page= requests.get(directory,headers=headers,timeout=30)
    soup = BeautifulSoup(page.content,"html.parser")
    for i in soup.find_all("a"):
        if ".xml" in str(i):
            link = i.get("href")
    return f"https://www.sec.gov/{link}"
