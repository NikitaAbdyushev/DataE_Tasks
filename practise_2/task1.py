import numpy as np
import json

file = "matrix_41.npy"
matrix = np.load(file)
main_diag = np.einsum("ii -> i", matrix)
side_diag = np.einsum("ii -> i", matrix[::-1])[::-1]
stat = {
    "sum": float(matrix.sum()),
    "avr": float(matrix.sum() / matrix.size),
    "sumMD": float(main_diag.sum()),
    "avrMD": float(main_diag.sum() / main_diag.size),
    "sumSD": float(side_diag.sum()),
    "avrSD": float(side_diag.sum() / side_diag.size),
    "max": float(matrix.max()),
    "min": float(matrix.min()),
}
with open("matrix_stat.json", "w") as f:
    f.write(json.dumps(stat))
np.save("norm_matrix", matrix / stat["sum"])
