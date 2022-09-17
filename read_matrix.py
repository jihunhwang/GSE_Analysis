from Progress import printProgressBar
import os


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

load()
