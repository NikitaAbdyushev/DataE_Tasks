from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter
import requests


def get_products(link) -> list():
    data = requests.get(link).text
    data = BeautifulSoup(data, "html.parser")
    products = data.find_all("div", attrs={"class": "pl-item-info"})
    items = list()
    for product in products:
        item = {
            "description": product.find("span", attrs={"style": "display: none"})
            .get_text()
            .strip(),
            "title": product.a["title"].strip(),
            "link": "https://ekb.rukzakoff.ru" + product.a["href"].strip(),
            "price": product.find("span", attrs={"class": "price nowrap"})
            .get_text()
            .replace("₽", "")
            .strip(),
        }
        if product.find("span", attrs={"class": "compare-at-price nowrap"}) == None:
            item["price without discount"] = (
                product.find("span", attrs={"class": "price nowrap"})
                .get_text()
                .replace("₽", "")
                .strip()
            )
        else:
            item["price without discount"] = (
                product.find("span", attrs={"class": "compare-at-price nowrap"})
                .get_text()
                .replace("₽", "")
                .strip()
            )
        if product.find("span", string=re.compile("Отзывов:")) == None:
            item["reviews"] = "0"
        else:
            item["reviews"] = (
                product.find("span", string=re.compile("Отзывов:"))
                .get_text()
                .strip()
                .split(" ")[1]
            )
        if product.find("div", attrs={"class": "stock-label stock-high"}) == None:
            item["availability"] = "Нет в наличии"
        else:
            item["availability"] = "В наличии"
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


def get_stat(
    list_of_dicts,
    key,
    sorter_func=lambda x: re.sub("[ .]", "", x).isdigit(),
) -> dict():
    stat = dict()
    title = key
    values = list()
    for item in list_of_dicts:
        if key in item.keys():
            values.append(str(item[key]))
    if all(map(sorter_func, values)):
        values = list(map(lambda x: float(re.sub("[^0-9.]", "", x)), values))
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
    sorted_items.sort(
        key=lambda x: float(re.sub("[^0-9.]", "", str(x[sorter_key]))), reverse=True
    )
    sorted_items += rest
    return sorted_items


def get_filtered(list_of_dicts, filter_key, filter_value, bool_key=True) -> list():
    filtered_items = list()
    if bool_key:
        for item in list_of_dicts:
            if (filter_key in item.keys()) and (
                item.get(filter_key, "no_such_key") == filter_value
            ):
                filtered_items.append(item)
    else:
        for item in list_of_dicts:
            if (filter_key in item.keys()) and (
                item.get(filter_key, "no_such_key") != filter_value
            ):
                filtered_items.append(item)
    return filtered_items


link = "https://ekb.rukzakoff.ru/category/ryukzaki"
raw_items = list()
for i in range(1, 10):
    raw_items += get_products(link + f"?page={i}")

items = get_sorted(raw_items, "price")
with open("result_5.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = get_filtered(items, "reviews", "0", False)
with open("result_5_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

items_stat = get_stat(items, "price") | get_stat(items, "availability")
with open("result_5_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items_stat, ensure_ascii=False))


def get_product(link) -> list():
    data = requests.get(link).text
    product = BeautifulSoup(data, "html.parser")
    item = {
        "name": product.find(
            "a",
            attrs={
                "itemprop": "item",
                "href": link,
            },
        )
        .find("span", attrs={"itemprop": "name"})
        .get_text()
        .strip(),
        "title": product.find("meta", attrs={"property": "og:title"})[
            "content"
        ].strip(),
        "description": product.find("meta", attrs={"property": "og:description"})[
            "content"
        ].strip(),
        "link": link,
        "img_url": product.find("meta", attrs={"property": "og:image"})[
            "content"
        ].strip(),
        "article": product.find(
            "span", attrs={"class": "value-article", "itemprop": "sku"}
        )
        .get_text()
        .strip(),
        "price": float(
            product.find("span", attrs={"class": "price nowrap"})
            .get_text()
            .replace("₽", "")
            .strip()
            .replace(" ", "")
        ),
    }
    if product.find("span", attrs={"class": "compare-at-price nowrap"}) == None:
        item["price without discount"] = float(
            product.find("span", attrs={"class": "price nowrap"})
            .get_text()
            .replace("₽", "")
            .strip()
            .replace(" ", "")
        )
    else:
        item["price without discount"] = float(
            product.find("span", attrs={"class": "compare-at-price nowrap"})
            .get_text()
            .replace("₽", "")
            .strip()
            .replace(" ", "")
        )
    if product.find("span", attrs={"class": "stock-label stock-high"}) != None:
        item["availability"] = "В наличии"
    elif product.find("span", attrs={"class": "stock-label stock-critical"}) != None:
        item["availability"] = (
            product.find("span", attrs={"class": "stock-label stock-critical"})
            .get_text()
            .strip()
        )
    else:
        item["availability"] = "Нет в наличии"
    features = product.find("table", attrs={"class": "features striped"}).find_all("tr")
    for feature in features:
        key = feature.find("td", attrs={"class": "name"}).contents[-1].strip()
        value = feature.find("td", attrs={"class": "value"}).get_text().strip()
        item[key] = value
    return item


links = list()
for item in raw_items:
    links.append(item["link"])

products = list()
for product_link in links[0:100]:
    products.append(get_product(product_link))

products = get_sorted(products, "Литраж")
with open("result_5_extended.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(products, ensure_ascii=False))

filtered_products = get_filtered(products, "Цвет", "Черный", True)
with open("result_5_extended_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

products_stat = get_stat(products, "Литраж", lambda x: True) | get_stat(
    products, "availability"
)
with open("result_5_extended_stat.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(products_stat, ensure_ascii=False))
