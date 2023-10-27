file_name = "text_2_var_41"
result_file = "result_2_var_41"
separators = ("|",)
clear_data = []
with open(file_name) as file:
    data = file.readlines()
for line in data:
    clear_data.append(
        list(
            map(
                int,
                (
                    "".join([ltr if ltr not in separators else " " for ltr in line])
                ).split(),
            )
        )
    )
with open(result_file, mode="w") as result:
    for line in clear_data:
        result.write(f"{sum(line) / len(line)}\n")
