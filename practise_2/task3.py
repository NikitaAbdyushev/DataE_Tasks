import json
import msgpack
import os

file = "products_41.json"
with open(file) as f:
    data = json.load(f)

products = dict()
result = list()
for item in data:
    if item["name"] in products.keys():
        products[item["name"]].append(item["price"])
    else:
        products[item["name"]] = list()
        products[item["name"]].append(item["price"])

for name, prices in products.items():
    result.append(
        {
            "name": name,
            "max price": max(prices),
            "min price": min(prices),
            "avr price": sum(prices) / len(prices),
        }
    )
with open("products_result.json", "w") as f:
    f.write(json.dumps(result))
with open("products_result.msgpack", "wb") as f:
    f.write(msgpack.dumps(result))

print(f"json size = {os.path.getsize('products_result.json')}")
print(f"msgpack size = {os.path.getsize('products_result.msgpack')}")
