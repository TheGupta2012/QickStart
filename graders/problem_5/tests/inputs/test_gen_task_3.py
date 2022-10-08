# Testcase generator for problem-5 task-3
import random

path = "task-3-"

for i in range(0, 10):
    N = [2, 4, 8, 16]
    n = random.choice(N)
    c = ["x", "y", "z"]
    l = []
    for j in range(0, n):
        a = random.uniform(-1, 1)
        l.append(a)

    f_path = path + str(i) + ".txt"

    file = open(f_path, mode="w", newline="\n")

    file.write(str(n) + "\n")

    for j in l:
        letter = random.choice(c)
        file.write(letter + " " + str(j) + "\n")

    file.close()
