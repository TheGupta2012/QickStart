# Testcase generator for problem-5 task-2
import random

path = "task-1-"

for i in range(0, 10):
    n = 4
    m = random.randint(1, 16)
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
