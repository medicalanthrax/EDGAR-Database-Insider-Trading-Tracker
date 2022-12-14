"""Contains collection()"""
import requests

def collection(year):
    """Get all the xml form 4 files from a given year"""
    good_data = []
    for i in range(1,5):        #For each of the four quarters
        url = f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{i}/form.idx"
        request = requests.get(
        url, headers={"User-Agent": "Carlo Tran carlotran4@gmail.com"}, timeout=30)
        data = request.text.split("\n")

        for i in data[0:-1]:
            if i[0] == "4":
                good_data.append(i)

    for idx,i in enumerate(good_data):              #Get only the dir links from each entry.
        good_data[idx] = f"https://www.sec.gov/Archives/{i[98:-13].replace('-','')}"

    print(good_data)
collection(2017)
