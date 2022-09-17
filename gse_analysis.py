import os
# import import_ipynb
# import pandas as pd
# import numpy as np
gse_file_name = 'GSE11886_series_matrix.txt'
# print(notebook_path)
print(gse_file_name)

GSE_file = open(gse_file_name, 'r')
n = 0

for item in GSE_file.readlines():
    n = n + 1
    # if(n >= 95):
    if(n > 1400):
        print(item)
    if(n == 2000):
        break
GSE_file.close()