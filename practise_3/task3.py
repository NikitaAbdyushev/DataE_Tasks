from bs4 import BeautifulSoup
import json
import numpy as np
from collections import Counter
from pathlib import Path


def get_item(file):
    with open(file, encoding="utf-8") as f:
        text = f.read()
    data = BeautifulSoup(text, "xml")
    item = {
        "name": data.find("name").get_text().strip(),
        "constellation": data.star.constellation.get_text().strip(),
        "spectral class": data.star.find("spectral-class").get_text().strip(),
        "radius": float(data.star.radius.get_text().strip()),
        "rotation": data.star.rotation.get_text().strip().split(" ")[0],
        "age": float(data.star.age.get_text().strip().split(" ")[0]),
        "distance": float(data.star.distance.get_text().strip().split(" ")[0]),
        "absolute-magnitude": data.star.find("absolute-magnitude")
        .get_text()
        .strip()
        .split(" ")[0],
    }
    return item


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


dir_name = "3_zip_var_41"
folder = Path(dir_name)
items = list()

for i in range(1, len(list(folder.iterdir()))):
    items.append(get_item(f"3_zip_var_41/{i}.xml"))

items.sort(key=lambda x: float(x["age"]), reverse=True)

with open("result_3.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = list()
for item in items:
    if item["constellation"] != "Козерог":
        filtered_items.append(item)

with open("result_3_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

stat = get_stat_from_dicts(items, "age") | get_stat_from_dicts(items, "constellation")
with open("result_3_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(stat, ensure_ascii=False))
