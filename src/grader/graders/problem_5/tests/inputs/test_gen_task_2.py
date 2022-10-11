# Testcase generator for problem-5 task-2
import random

path = "task-2-"

for i in range(0, 10):
    N = [2, 4, 8, 16]
    n = random.choice(N)
    m = random.randint(1, 128)
    l = []
    for j in range(0, n):
        a = random.randint(1, m)
        l.append(a)

    f_path = path + str(i) + ".txt"

    file = open(f_path, mode="w", newline="\n")

    file.write(str(n) + " " + str(m) + "\n")

    for j in l:
        file.write(str(j) + " ")
    file.write("\n")

    file.close()
