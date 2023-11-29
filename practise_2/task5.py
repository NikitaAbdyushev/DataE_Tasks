import csv
import numpy as np
from collections import Counter
import json
import pickle
import msgpack
import os


def get_stat(array):
    stat = dict()
    for column in array.T:
        title = column[0]
        if all(map(lambda x: x.replace(".", "").isdigit(), column[1:])):
            values = list(map(float, column[1:]))
            stat[title] = {
                "sum": round(sum(values), 3),
                "avr": round(sum(values) / len(values), 3),
                "max": round(max(values), 3),
                "min": round(min(values), 3),
                "std": round(np.std(values), 3),
            }
        else:
            stat[title] = dict(Counter(column[1:]))
    return stat


def csv_in_json(array):
    dataset = dict()
    for column in array.T:
        dataset[column[0]] = list(column[1:])
    return dataset


file = "Border_Crossing_Entry_Data.csv"
data = list()
with open(file, encoding="utf-8") as f:
    for line in csv.reader(f):
        data.append(line[1:-1])
data = np.array(data)
stat = get_stat(data)

with open("result_5.json", "w") as f:
    f.write(json.dumps(stat))

data = csv_in_json(data)
with open("dataset_5.json", "w") as f:
    f.write(json.dumps(data))

with open("dataset_5.msgpack", "wb") as f:
    f.write(msgpack.dumps(data))

with open("dataset_5.pkl", "wb") as f:
    f.write(pickle.dumps(data))

print(f"csv size = {os.path.getsize('Border_Crossing_Entry_Data.csv')}")
print(f"json size = {os.path.getsize('dataset_5.json')}")
print(f"msgpack size = {os.path.getsize('dataset_5.msgpack')}")
print(f"pickle size = {os.path.getsize('dataset_5.pkl')}")
