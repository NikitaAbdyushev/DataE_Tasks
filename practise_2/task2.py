import numpy as np
import os

file = "matrix_41_2.npy"
matrix = np.load(file)
xyz = np.array(
    [[[i, j, val] for j, val in enumerate(line)] for i, line in enumerate(matrix)]
).reshape(-1, 3)
xyz_filtered = np.array([i for i in xyz if i[2] > 541])
np.savez("points", x=xyz_filtered[:, 0], y=xyz_filtered[:, 1], z=xyz_filtered[:, 2])
np.savez_compressed(
    "points_zip", x=xyz_filtered[:, 0], y=xyz_filtered[:, 1], z=xyz_filtered[:, 2]
)

print(f"points size = {os.path.getsize('points.npz')}")
print(f"points_zip size = {os.path.getsize('points_zip.npz')}")
