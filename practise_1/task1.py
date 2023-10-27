from collections import Counter
import string

file_name = "text_1_var_41"
result_file = "result_1_var_41"
with open(file_name) as file:
    data = file.read()
data = (
    "".join([ltr if ltr not in string.punctuation else " " for ltr in data])
).split()
cnt = Counter(data)
sorted_cnt = sorted(cnt.items(), key=lambda x: x[1], reverse=True)
with open(result_file, mode="w") as result:
    for word, freq in sorted_cnt:
        result.write(f"{word}:{freq}\n")
