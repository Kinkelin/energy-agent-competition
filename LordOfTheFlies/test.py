import numpy as np

a1 = np.random.randint(0,10,size=(3,3))
a2 = np.full((2,2), 1)
a3 = np.kron(a1,a2)
print(a1)
print(a3)