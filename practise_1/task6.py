from bs4 import BeautifulSoup
import json
import requests

result_file = "result_6.html"
API_link = r"https://www.gov.uk/bank-holidays.json"
response = requests.get(API_link)
data = json.loads(response.text)
# print(data.keys())
soup = BeautifulSoup(
    "<html><head><title>Bank Holidays</title></head><body></body></html>",
    features="html.parser",
)
result = soup.html
body_tag = soup.body
for bank in data.keys():
    new_table_tag = soup.new_tag("table")
    new_title_tag = soup.new_tag("p", class_="title")
    new_b_tag = soup.new_tag("b")
    new_b_tag.string = bank
    new_title_tag.append(new_b_tag)
    new_tr_tag = soup.new_tag("tr")
    for title in data[bank]["events"][0].keys():
        new_th_tag = soup.new_tag("th")
        new_th_tag.string = title
        new_tr_tag.append(new_th_tag)
    new_table_tag.append(new_tr_tag)
    for event in data[bank]["events"]:
        new_tr_tag = soup.new_tag("tr")
        for key in event.keys():
            new_td_tag = soup.new_tag("td")
            new_td_tag.string = str(event[key])
            new_tr_tag.append(new_td_tag)
        new_table_tag.append(new_tr_tag)
    body_tag.append(new_title_tag)
    body_tag.append(new_table_tag)
with open(result_file, "w") as f:
    f.write(result.prettify())
