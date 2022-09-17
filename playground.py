import numpy as np

M = np.array([[]])
v = [[1, 2, 3]]
for _ in range(3):
    N = np.append(M, v, axis=0)

print(N)
print(np.transpose(M))

trans = np.transpose(M)
print(trans.shape)