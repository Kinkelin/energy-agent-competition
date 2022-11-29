import numpy as np

a1 = np.full((6,6), 3)

a2 = np.full((6,6), 3)


print(a1)
print(a2)

a_change = np.where(a1 != a2)


for i in range(len(a_change[0])):
    print(a_change[0][i],a_change[1][i], a2[a_change[0][i],a_change[1][i]])