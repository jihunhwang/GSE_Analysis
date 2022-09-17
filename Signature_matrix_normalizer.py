import numpy as np
import pandas as pd

# Signature matrix normalizer
# 	Written by Jihun Hwang. Minor bugs fixed by Wenbo Xie
from numpy.core._multiarray_umath import ndarray

new_matrix = []
f = open('matrix_raw.txt', 'r')
while True:
    l = f.readline()
    if not l:
        break
    new_l = np.array(l.split(','))
    new_ll = new_l[:-1]
    new_lll = []
    for i in new_ll:
        i = i.replace(',', '.')
        i = float(i)
        new_lll.append(i)
    # print(new_lll)
    new_matrix.append(new_lll)


normalized_matrix = np.array([[]])
count = 0
max_length = 0

for rows in new_matrix:
    norm = np.linalg.norm(rows)
    new_row = np.array([[x / norm for x in rows]])
    # print(len(new_row[0]))
    if max_length <= (new_row[0]).size:
        max_length = new_row[0].size
    # print(max_length)

for rows in new_matrix:
    norm = np.linalg.norm(rows)
    new_row = np.array([[x/norm for x in rows]])
    # print(np.shape(new_row))
    # print(len(new_row))
    if max_length > (new_row[0]).size:
        num_of_zeros = max_length-len(new_row[0])
        print(num_of_zeros)
        for i in range(0, num_of_zeros):
            new_row = np.append(new_row, 0)
        print(np.shape(new_row))
        new_row = np.reshape(new_row, (1, max_length))
        # placeholder = np.zeros((num_of_zeros, 1))
        # print(np.shape(placeholder))
        # new_new_row = np.concatenate((new_row, placeholder), axis=1)
        # new_new_row = np.array(new_new_row)
        # print(np.shape(new_new_row))
        # new_row = np.reshape(new_new_row, (max_length, 1))
    new_col = np.transpose(new_row)
    # print(np.shape(new_row))
    # print(np.shape(new_col))

    if count == 0:
        normalized_matrix = new_col
        count = count + 1
    # normalized_matrix.append(new_row.tolist())
    else:
        print(np.shape(normalized_matrix))
        print(np.shape(new_row))
        normalized_matrix = np.concatenate((normalized_matrix, new_row.T), axis=1)

# normalized_matrix = np.array(normalized_matrix)
# print(normalized_matrix)
print(normalized_matrix.shape)
# print(normalized_matrix)
# normalized_matrix = np.matrix(normalized_matrix)[np.newaxis]

# transposed_norm_mat = list(map(normalized_matrix, zip(*l)))
# transposed_norm_mat = np.transpose(normalized_matrix)
# print(transposed_norm_mat.shape)

with open('signature_matrix_colon.txt', 'w') as f:
    for rows in normalized_matrix:
        for item in rows:
            f.write("{},".format(item))
        f.write('\n')

# print(np.shape(transposed_norm_mat))
# print(np.shape(normalized_matrix))
