import json
import pickle


def update_price(product, price_info):
    method = price_info["method"]
    if method == "sum":
        product["price"] += price_info["param"]
    elif method == "sub":
        product["price"] -= price_info["param"]
    elif method == "percent+":
        product["price"] *= 1 + price_info["param"]
    elif method == "percent-":
        product["price"] *= 1 - price_info["param"]


with open("products_41.pkl", "rb") as f:
    products = pickle.load(f)

with open("price_info_41.json") as f:
    price_info = json.load(f)

info_dict = dict()

for item in price_info:
    info_dict[item["name"]] = item

for product in products:
    update_price(product, info_dict[product["name"]])

with open("products_updated.pkl", "wb") as f:
    f.write(pickle.dumps(products))
