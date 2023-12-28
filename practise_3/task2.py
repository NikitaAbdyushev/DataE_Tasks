from bs4 import BeautifulSoup
import json
import numpy as np
from collections import Counter
from pathlib import Path


def get_products(file):
    with open(file, encoding="utf-8") as f:
        text = f.read()
    data = BeautifulSoup(text, "html.parser")
    products = data.find_all("div", attrs={"class": "product-item"})
    items = list()
    for product in products:
        item = {
            "id": int(data.a["data-id"].strip()),
            "link": data.find_all("a")[1]["href"].strip(),
            "img_url": data.img["src"].strip(),
            "title": data.span.get_text().strip(),
            "price": float(
                data.price.get_text().replace("₽", "").strip().replace(" ", "")
            ),
            "bonus": float(data.strong.get_text().strip().split(" ")[2]),
        }
        specifications = product.ul.find_all("li")
        for spec in specifications:
            item[spec["type"]] = spec.get_text().strip()
        items.append(item)
    return items


def get_stat_from_dicts(list_of_dicts, key):
    stat = dict()
    title = key
    values = list()
    for item in list_of_dicts:
        values.append(str(item[key]))
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


dir_name = "2_zip_var_41"
folder = Path(dir_name)
items = list()

for i in range(1, len(list(folder.iterdir())) + 1):
    items += get_products(dir_name + f"/{i}.html")

items.sort(key=lambda x: float(x["id"]), reverse=True)

with open("result_2.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = list()
for item in items:
    if item["title"] != '6.0" Seagate 160GB':
        filtered_items.append(item)

with open("result_2_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

stat = get_stat_from_dicts(items, "price") | get_stat_from_dicts(items, "title")
with open("result_2_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(stat, ensure_ascii=False))
