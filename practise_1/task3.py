separators = (",",)
filtered_data = []
file_name = "text_3_var_41"
result_file = "result_3_var_41"
with open(file_name) as file:
    data = file.readlines()
for line in data:
    filtered_data.append(
        ("".join([ltr if ltr not in separators else " " for ltr in line])).split(),
    )
filtered_data = [
    list(
        filter(
            lambda x: x ** (0.5) >= 91,
            [
                int(num)
                if num.isdigit()
                else int((int(line[i - 1]) + int(line[i + 1])) / 2)
                for i, num in enumerate(line)
            ],
        )
    )
    for line in filtered_data
]
with open(result_file, mode="w") as result:
    for line in filtered_data:
        result.write(f"{line[0]}")
        for word in line[1:]:
            result.write(f",{word}")
        result.write("\n")
