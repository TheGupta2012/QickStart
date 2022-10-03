from qiskit import execute, QuantumCircuit
from qiskit import Aer
from math import pi

# some global values
PI_2 = pi / 2
correct_stmt = "Congratulations your answer is correct!!"
wrong_stmt = "Uh-oh, that's not quite correct"

# quantum stuff
qasm_backend = Aer.get_backend("qasm_simulator")

# utils
def initialize(state, qc):
    if state == "1":
        qc.x(0)
    elif state == "+":
        qc.h(0)
    elif state == "-":
        qc.x(0)
        qc.h(0)
    elif state == "r":
        qc.h(0)
        qc.s(0)
    elif state == "l":
        qc.h(0)
        qc.rz(-PI_2, 0)


def get_circuit(state, r1, r2, r3):

    qc = QuantumCircuit(1)
    # can't use initialize, dk why
    initialize(state, qc)

    # apply rotations
    qc.rz(r1 * PI_2, 0)
    qc.rx(r2 * PI_2, 0)
    qc.ry(r3 * PI_2, 0)
    qc.measure_all()

    return qc


class grader1:
    state_set = {"0", "1", "-", "+", "r", "l"}

    @classmethod
    def evaluate(cls, generate_bloch_operation):
        # we will evaluate it on different states

        correct = 0
        for state in cls.state_set:
            # user code
            try:
                rotations = generate_bloch_operation(state)

                # execute and check
                circuit = get_circuit(state, rotations[0], rotations[1], rotations[2])
                result = execute(circuit, qasm_backend).result()
                counts = result.get_counts()

            except:
                break
            # correct circuit if only 0 present
            if len(counts) == 1 and "0" in counts.keys():
                correct += 1

        if correct == len(cls.state_set):
            # do something with the API
            json_response = {}

            # return something to the jupyter notebook
            print(correct_stmt)
        else:
            # do something with the API

            # return something to the jupyter notebook
            print(wrong_stmt)


class grader2:
    input_path = "tests/input/task-2-"
    # path is like 2-1, 2-2, 2-3, ...

    @classmethod
    def _check_circuit(cls, state, circuit):

        qc = QuantumCircuit(1)
        initialize(state, qc)
        qc.compose(circuit, qubits=[0], inplace=True)
        qc.measure_all()
        result = execute(qc, qasm_backend, shots=10).result()
        counts = result.get_counts()

        return len(counts) == 1 and "0" in counts.keys()

    @classmethod
    def evaluate(cls, get_total_bloch_ops):
        # run the tests

        for test in range(10):
            test_input_path = cls.input_path + str(test) + ".txt"

            file_rows = open(test_input_path).readlines()
            # the first line is the state
            state = file_rows[0][0]

            # other lines are the lists
            arz, arx, ary = (
                file_rows[1][:-1].split(","),
                file_rows[2][:-1].split(","),
                file_rows[3][:-1].split(","),
            )

            print(arz, arx, ary)
            n, m, k = len(arz), len(arx), len(ary)

            # user operation
            user_total, user_bloch_ops = get_total_bloch_ops(state, arz, arx, ary)

            # incorrect
            if user_total != len(user_bloch_ops):
                # wrong answer
                # do something to API

                print(wrong_stmt)
                return

            # now check
            total_bloch_ops = 0
            bloch_ops = set()

            # now build our own
            for i in range(n):
                for j in range(m):
                    for s in range(k):
                        circuit = get_circuit(
                            state, int(arz[i]), int(arx[j]), int(ary[s])
                        )

                        result = execute(circuit, qasm_backend, shots=10).result()
                        counts = result.get_counts()

                        if len(counts) == 1 and "0" in counts.keys():
                            total_bloch_ops += 1
                            bloch_ops.add((i, j, s))
                            # print("Adding ", i, j, s)

            # now search
            condition1 = user_total == total_bloch_ops

            condition2 = True

            # check
            for bloch_op in user_bloch_ops:
                try:
                    print(bloch_op)
                    if bloch_op[0] in bloch_ops and cls._check_circuit(
                        state, bloch_op[1]
                    ):
                        print(bloch_op[1].draw())
                        continue
                    else:
                        condition2 = False
                        break
                except:
                    condition2 = False
                    break

            if condition1 and condition2:
                # continue for other tests
                continue
            else:
                # do something in API

                # return wrong stmt

                print(wrong_stmt)
                return

        # correct
        # do something to api

        print(correct_stmt)


class grader3:
    input_path = "tests/input/task-3.txt"
    output_path = "tests/output/task-3.txt"

    # here only the comparison needs to be done

    # to do...
