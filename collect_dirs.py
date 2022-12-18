"""Contains collect_dirs"""
import re

import requests
from bs4 import BeautifulSoup


def collect_dirs(url="https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=4&owner=only&count=100&action=getcurrent"):
    """ Collect all the directories to the EDGAR xml files that have not yet been parsed.

    Returns: list of directories to links to xml files
    """
    headers = {
        "User-Agent": "Carlo Tran carlotran4@gmail.com"
    }

    acc_no = []
    cik = []
    num = 0  # iterator for getting new pages
    while True:
        page = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(page.content, "html.parser")
        page.close()

        # Get all Acc No's
        for i in soup.find_all(string=re.compile("Accession Number:")):
            i = i.replace("Accession Number: ", "")
            i = i.split()[0]
            acc_no.append(i)

        # Get all CIK's
        for i in soup.find_all("a"):
            i = str(i)
            if "cgi-bin" in i and "file" not in i and "getcurrent" not in i:
                cik.append(i[57:67])

        file = open("acc_nos.txt", "r", encoding="utf-8")
        matches = False
        print(acc_no[len(acc_no)-1])
        for line in file:
            if acc_no[len(acc_no)-1] == line[0:len(line)-1]:
                matches = True
        file.close()

        if matches:
            break
        else:
            num += 100
            print(f"going to page{num/100+1}")
            url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=only&accno=&start={num}&count=100"

    # remove duplicate acc_no's.
    temp = []
    temp_cik = []
    for i in range(len(acc_no)):        # pylint: disable = consider-using-enumerate
        if acc_no[i] not in temp:
            temp.append(acc_no[i])
            temp_cik.append(cik[i])
    acc_no = temp
    cik = temp_cik

    # Exclude links that have already been collected
    file = open("acc_nos.txt", "r", encoding="utf-8")
    for line in file:
        for i in acc_no:
            if i == line[0:len(line)-1]:
                cik.pop(acc_no.index(i))
                acc_no.remove(i)       # pylint: disable = W4701

    # append new acc No's to file.
    file.close()
    file = open("acc_nos.txt", "a", encoding="utf-8")
    for i in acc_no:
        file.write(i+"\n")
    links = []
    for i in range(len(acc_no)):        # pylint: disable = consider-using-enumerate
        links.append(
            f"https://www.sec.gov/Archives/edgar/data/{cik[i]}/{re.sub(r'[^0-9]','',acc_no[i])}")
    print(f"No. of links added: {len(acc_no)}")
    return links
