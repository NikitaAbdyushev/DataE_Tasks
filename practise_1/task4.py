import csv

data = []
avg_salary = 0
file_name = "text_4_var_41"
result_file = "result_4_var_41.csv"
with open(file_name, encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    for line in reader:
        unit = {
            "id": int(line[0]),
            "name": line[2] + " " + line[1],
            "age": int(line[3]),
            "salary": int(line[4][:-1]),
        }
        data.append(unit)
        avg_salary += unit["salary"]
avg_salary /= len(data)
filtered_data = list(
    filter(lambda x: (x["salary"] >= avg_salary) and (x["age"] > 26), data)
)
filtered_data.sort(key=lambda x: x["id"])
with open(result_file, mode="w", encoding="utf-8") as result:
    writer = csv.writer(result, delimiter=",")
    for line in filtered_data:
        writer.writerow(line.values())
