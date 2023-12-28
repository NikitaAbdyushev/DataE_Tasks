from bs4 import BeautifulSoup
import json
import numpy as np
from collections import Counter
from pathlib import Path


def get_products(file) -> list():
    with open(file, encoding="utf-8") as f:
        text = f.read()
    data = BeautifulSoup(text, "xml")
    products = data.find_all("clothing")
    items = list()
    for product in products:
        item = dict()
        content = product.contents
        while "\n" in content:
            content.remove("\n")
        for property in content:
            item[property.name] = property.get_text().strip()
        items.append(item)
    keys = set()
    for item in items:
        keys.update(item.keys())
    for key in keys:
        items_with_key = filter(lambda x: key in x.keys(), items)
        if all(
            map(
                lambda x: x[key].replace(".", "").replace(" ", "").isdigit(),
                items_with_key,
            )
        ):
            for item in items:
                if key in item.keys():
                    item[key] = float(item[key].replace(" ", ""))
    return items


def get_stat(list_of_dicts, key) -> dict():
    stat = dict()
    title = key
    values = list()
    for item in list_of_dicts:
        if key in item.keys():
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


def get_sorted(list_of_dicts, sorter_key) -> list():
    sorted_items = list()
    rest = list()
    for item in list_of_dicts:
        if sorter_key in item.keys():
            sorted_items.append(item)
        else:
            rest.append(item)
    sorted_items.sort(key=lambda x: float(x[sorter_key]), reverse=True)
    sorted_items += rest
    return sorted_items


def get_filtered(list_of_dicts, filter_key, filter_value) -> list():
    filtered_items = list()
    for item in list_of_dicts:
        if (filter_key in item.keys()) & (
            item.get(filter_key, "no_such_key") == filter_value
        ):
            filtered_items.append(item)
    return filtered_items


dir_name = "4_zip_var_41"
folder = Path(dir_name)
items = list()

for i in range(1, len(list(folder.iterdir())) + 1):
    items += get_products(dir_name + f"/{i}.xml")

items = get_sorted(items, "rating")
with open("result_4.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = get_filtered(items, "new", "+")
with open("result_4_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

stat = get_stat(items, "price") | get_stat(items, "material")
with open("result_4_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(stat, ensure_ascii=False))

print(stat)
