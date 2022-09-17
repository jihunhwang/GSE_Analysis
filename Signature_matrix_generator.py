from Progress import printProgressBar
import os
import numpy as np

# Signature matrix generator
# 	Written by Wenbo Xie.
#	Normalization added, minor mistakes fixed by Jihun Hwang.

# Step 1) Make a new directory "/data/matrices/" under this directory
# Step 2) Save the GSE series matrix txt files in "/data/matrices/" folder
# Step 3) Run this code using Python interpreter

# Outputs
# 	(1) matrix_raw.txt : Un-normalized transposed signature matrix
#               Saved in case we need it (also, used to compute signature_matrix.txt)
# 	(2) signature_matrix.txt : The Signature matrix we are looking for


def read_matrix(filename):
    import numpy as np
    ID = False
    col_labels = None
    col_labels_found = False

    probe_ids = np.array([], dtype=np.str)
    values = []
    BarLength = 50
    with open(filename, 'r', encoding="utf8") as f:
        lines = f.readlines()
        l = len(lines)
        printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete, Current: 0',
                         length = BarLength)
        for i, line in enumerate(lines):
            # print(line >= "!series_matrix_table_begin")
            if ID == False and line >= "!series_matrix_table_begin":
                ID = True 
                continue
            if ID:
                buff = line.split()
                if not col_labels_found:
                    col_labels = np.array(buff, dtype=np.str)
                    col_labels_found = True
                else:
                    if buff[0][1:-1] != "series_matrix_table_en":
                        probe_ids = np.append(probe_ids, buff[0][1:-1])
                    values += [np.mean(np.array(buff[1:], dtype=np.float))]
                    # values = np.concatenate((values, np.array(buff[1:], dtype=np.float)))
            printProgressBar(i+1, l, prefix = 'Progress:', suffix = 'Complete, Current: {}'.format(i+1),
                             length = BarLength)
    values = np.array(values)
    # print(buff)
    print(probe_ids)
    return (probe_ids, values)
    # print(probe_ids[1], values[1])


def load():
    import numpy as np
    # filenames = 
    # ids = None
    # BarLength = 50
    matrix_raw = []
    for _, _, filenames in os.walk("data/matrices/"):
        # l = len(filenames)
        for filename in filenames:
            print(filename)
            col = None
            # if ids == None:
            #     # ids, col = read_matrix("data/matrices/" + filename)
            # else:
            _, col = read_matrix("data/matrices/" + filename)
            matrix_raw += [col[~np.isnan(col)]]
            # print(ids.shape, col.shape)

    with open('matrix_raw.txt', 'w') as f:
        for line in matrix_raw:
            for item in line:
                f.write("{},".format(item))
            f.write('\n')
    # np.savetxt('symbols.txt', ids, delimiter=',')
    # with open(symbols)


def normalization():
    # Scan matrix_raw.txt, convert it into a matrix
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

    # new_matrix is still transposed and not normalized.
    # normalize the rows of new_matrix first, then transpose them.
    normalized_matrix = np.array([[]])
    count = 0
    max_length = 0

    # Some GSE's have smaller number of data, zeros will be added as a placeholder.
    for rows in new_matrix:
        norm = np.linalg.norm(rows)
        new_row = np.array([[x / norm for x in rows]])
        # print(len(new_row[0]))
        if max_length <= (new_row[0]).size:
            max_length = new_row[0].size
        # print(max_length)

    for rows in new_matrix:
        norm = np.linalg.norm(rows)
        new_row = np.array([[x / norm for x in rows]])
        # print(np.shape(new_row))
        # print(len(new_row))
        if max_length > (new_row[0]).size:
            num_of_zeros = max_length - len(new_row[0])
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

    with open('signature_matrix_finalized.txt', 'w') as f:
        for rows in normalized_matrix:
            for item in rows:
                f.write("{},".format(item))
            f.write('\n')

    # print(np.shape(transposed_norm_mat))
    # print(np.shape(normalized_matrix))

def main():
    load()
    normalization()

if __name__ == "__main__":
    main()
