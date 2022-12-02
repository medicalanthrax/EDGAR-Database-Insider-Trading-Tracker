"""Contains collect_links"""
import re
import requests
from bs4 import BeautifulSoup


def collect_links(url = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=4&owner=only&count=100&action=getcurrent"):
    """ Collect all the EDGAR links that have not yet been parsed

    Returns list of links to xml files
    """
    headers = {
        "User-Agent": "Carlo Tran carlotran4@gmail.com"
    }
    page = requests.get(url, headers=headers, timeout=30)

    soup = BeautifulSoup(page.content, "html.parser")
    page.close()
    # Get all Acc No's
    acc_no = []
    for i in soup.find_all(string=re.compile("Accession Number:")):
        i = i.replace("Accession Number: ", "")
        i = i.split()[0]
        acc_no.append(i)

    # Get all CIK's
    cik = []
    for i in soup.find_all("a"):
        i = str(i)
        if "cgi-bin" in i and "file" not in i and "getcurrent" not in i:
            cik.append(i[57:67])

    #remove duplicate acc_no's.
    temp = []
    temp_cik = []
    for i in range(100):
        if acc_no[i] not in temp:
            temp.append(acc_no[i])
            temp_cik.append(cik[i])
    acc_no = temp
    cik = temp_cik

    #Exclude links that have already been collected
    file = open("acc_nos.txt","r",encoding="utf-8")
    amount_removed = 0      #Keep track of how many you removed: 0 means go to next page.
    for line in file:
        for i in acc_no:
            if i == line[0:len(line)-1]:
                amount_removed+=1
                cik.pop(acc_no.index(i))
                acc_no.remove(i)

    #append new acc No's to file.
    file.close()
    file = open("acc_nos.txt","a",encoding="utf-8")
    for i in acc_no:
        file.write(i+"\n")

    return()
collect_links()



"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=only&accno=&start=100&count=100"