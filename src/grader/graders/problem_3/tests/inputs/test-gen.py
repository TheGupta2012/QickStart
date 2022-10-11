import numpy as np

states = ["0", "1", "+", "-", "r", "l"]


def generate_tests(init_path, limit_n, limit_m, limit_k):
    for i in range(10):
        f_path = init_path + str(i) + ".txt"
        n, m, k = (
            np.random.randint(1, limit_n),
            np.random.randint(1, limit_m),
            np.random.randint(1, limit_k),
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


path_2 = "task-2-"
path_3 = "task-3-"

generate_tests(path_2, 10, 10, 10)
generate_tests(path_3, 100000, 100000, 100000)
