from bs4 import BeautifulSoup
import csv

data = []
file_name = "text_5_var_41"
result_file = "result_5_var_41.csv"
with open(file_name, encoding="utf-8") as f:
    soup = BeautifulSoup(f, features="html.parser")
    title = soup.find_all("tr")[0].find_all("th")
    # print(title)
    for unit in soup.find_all("tr")[1:]:
        info = unit.find_all("td")
        item = {title[i].text: info[i].text for i in range(len(title))}
        data.append(item)
print(data)
with open(result_file, mode="w", encoding="utf-8") as result:
    writer = csv.writer(result, delimiter=",")
    for line in data:
        writer.writerow(line.values())
