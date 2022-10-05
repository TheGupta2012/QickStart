import numpy as np
import random

# print(np.random.binomial(n=1, p=0.5, size=[10]))
path = "task-3-"

for i in range(0, 10):
    f_path = path + str(i) + ".txt"
    N = [4, 8, 16, 32]
    n = random.choice(N)
    k = random.randint(1, 6)

    b = []
    c = []

    file = open(f_path, mode="w", newline="\n")
    file.write(str(n) + " " + str(k) + "\n")

    if k > 2:
        for j in range(0, k - 2):
            b.append(np.random.binomial(n=1, p=0.5, size=[n]))
        c.append(np.ones(n))
        c.append(np.zeros(n))

    else:
        for j in range(0, k):
            b.append(np.random.binomial(n=1, p=0.5, size=[n]))

    for j in b:
        file.write("B\n")
        for k in j:
            file.write(str(k) + " ")
        file.write("\n")

    for j in c:
        file.write("C\n")
        for k in j:
            file.write(str(int(k)) + " ")
        file.write("\n")

    file.close()
