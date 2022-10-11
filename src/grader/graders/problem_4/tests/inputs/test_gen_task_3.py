import numpy as np
import random

# print(np.random.binomial(n=1, p=0.5, size=[10]))
path = "task-3-"
for i in range(0, 10):
    f_path = path + str(i) + ".txt"

    N = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    n = random.choice(N)

    file = open(f_path, mode="w", newline="\n")

    f_type = ["B", "C"]

    curr_type = random.choice(f_type)

    if curr_type == "B":

        function = np.random.binomial(n=1, p=0.5, size=[n])
        while sum(function) != n / 2:
            function = np.random.binomial(n=1, p=0.5, size=[n])
    else:
        if random.randint(0, 1):
            function = np.ones(n)
        else:
            function = np.zeros(n)
    function = [int(x) for x in function]

    # add the type first
    file.write(f"{curr_type}\n")
    #     file.write(str(function))
    file.write("[")
    ##fi
    for i, j in enumerate(function):
        file.write(str(int(j)))
        if i != (n - 1):
            file.write(",")
    file.write("]")

    file.write("\n")

    file.close()
