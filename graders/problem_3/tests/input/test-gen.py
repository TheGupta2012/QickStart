import numpy as np

path = "task-2-"

states = ["0", "1", "+", "-", "r", "l"]

for i in range(1, 10):
    f_path = path + str(i) + ".txt"
    n, m, k = (
        np.random.randint(1, 50),
        np.random.randint(1, 50),
        np.random.randint(1, 50),
    )

    arz = [np.random.randint(-1e3, 1e3) for _ in range(n)]
    arx = [np.random.randint(-1e3, 1e3) for _ in range(m)]
    ary = [np.random.randint(-1e3, 1e3) for _ in range(k)]

    state = np.random.choice(states)

    file = open(f_path, mode="w", newline="\n")

    file.write(state + "\n")

    def write_list(file, l, size):
        for i, z in enumerate(l):
            file.write(str(z))
            if i != size - 1:
                file.write(",")
        file.write("\n")

    write_list(file, arz, n)
    write_list(file, arx, m)
    write_list(file, ary, k)

    file.close()
