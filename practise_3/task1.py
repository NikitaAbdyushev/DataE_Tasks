from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter
from pathlib import Path


def get_item(file):
    with open(file, encoding="utf-8") as f:
        text = f.read()
    data = BeautifulSoup(text, "html.parser")
    item = {
        "genre": data.find("span", string=re.compile("Категория:"))
        .get_text()
        .split(":")[1]
        .strip(),
        "title": data.find("h1", {"class": "book-title"}).get_text().strip(),
        "author": data.find("p", {"class": "author-p"}).get_text().strip(),
        "pages": data.find("span", attrs={"class": "pages"})
        .get_text()
        .split(":")[1]
        .strip(),
        "year": data.find("span", attrs={"class": "year"})
        .get_text()
        .split("в")[1]
        .strip(),
        "ISBN": data.find("span", string=re.compile(r"ISBN:"))
        .get_text()
        .split(":")[1]
        .strip(),
        "description": data.find("p", string=re.compile(r"Описание"))
        .get_text()
        .split("Описание")[1]
        .strip(),
        "img_url": data.find("img")["src"],
        "rating": data.find("span", string=re.compile(r"Рейтинг:"))
        .get_text()
        .split(":")[1]
        .strip(),
        "views": data.find("span", string=re.compile(r"Просмотры:"))
        .get_text()
        .split(":")[1]
        .strip(),
    }
    return item


def get_stat_from_dicts(list_of_dicts, key):
    stat = dict()
    title = key
    values = list()
    for item in list_of_dicts:
        values.append(item[key])
    if all(map(lambda x: x.replace(".", "").replace(" ", "").isdigit(), values)):
        values = list(map(lambda x: float(x.replace(" ", "")), values))
        stat[title] = {
            "sum": round(sum(values), 3),
            "avr": round(sum(values) / len(values), 3),
            "max": round(max(values), 3),
            "min": round(min(values), 3),
            "std": round(np.std(values), 3),
        }
    else:
        stat[title] = dict(Counter(values))
    return stat


dir_name = "1_zip_var_41"
folder = Path(dir_name)
items = list()

for i in range(1, len(list(folder.iterdir()))):
    items.append(get_item(f"1_zip_var_41/{i}.html"))

items.sort(key=lambda x: float(x["rating"]), reverse=True)

with open("result_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items = list()
for item in items:
    if item["genre"] != "любовный роман":
        filtered_items.append(item)

with open("result_1_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

stat = get_stat_from_dicts(items, "rating") | get_stat_from_dicts(items, "genre")
with open("result_1_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(stat))
