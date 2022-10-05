# simple graph problem
import signal
from contextlib import contextmanager
from qiskit import execute, QuantumCircuit, Aer

import requests

# for the time out management


class TimeOutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeOutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


INPUT_PATH = "graders/problem_4/tests/inputs/"
OUTPUT_PATH = "graders/problem_4/tests/outputs/"

CORRECT_STMT = "Congratulations, your answer is correct!"
WRONG_STMT = "Uh-oh, that's not quite correct :("
SERVER_STMT = "The server couldn't process your request correctly at the moment, please try again in a while"
TIME_STMT = "Uh-oh, time limit exceeded for the problem :("

QBRAID_API = None
BACKEND = Aer.get_backend("qasm_simulator")


def test_loader_1(file_path):
    # make it faster ...
    with open(file_path, "r") as file:

        for row_id, row in enumerate(file):
            if row_id == 0:
                f_type = row[0]
            else:
                test_function = [int(x) for x in row[1:-1].split(",")]

    return f_type, test_function


def test_loader_2(file_path):
    # make it faster ...
    with open(file_path, "r") as file:
        f_types, test_functions = [], []

        for row_id, row in enumerate(file):
            if row_id == 0:
                N, K = row[0].split()
                N, K = int(N), int(K)
            else:
                if row_id % 2 == 1:
                    # odd row, has type of function
                    f_type = row[0]
                    f_types.append(f_type)
                else:
                    test_function = [int(x) for x in row[1:-1].split(",")]
                    test_functions.append(test_function)

    return N, K, f_types, test_functions


def get_dj_circuit(size, user_oracle):
    qc = QuantumCircuit(size, size - 1)

    # last qubit should be in |-> state
    qc.x(size - 1)
    qc.h(range(size))

    qc.barrier()
    qc.compose(user_oracle, qubits=list(range(size)), inplace=True)
    qc.barrier()

    qc.h(range(size))

    qc.measure(list(range(size - 1)), list(range(size - 1)))

    return qc


class grader1:
    ip_task_path = INPUT_PATH + "task-1-"
    op_task_path = OUTPUT_PATH + "task-1-"
    dj_qubits = 2
    total_tests = 10
    time_limit = 20

    return_json = {
        "team-id": None,
        "problem": {"4.1": {"points": "50", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        return "123"

    @staticmethod
    def run(dj_oracle_2q):

        correct = 0
        # load your tests here
        for test in range(grader1.total_tests):
            ip_test_path = grader1.ip_task_path + str(test) + ".txt"
            func_type, function = test_loader_1(ip_test_path)
            try:
                user_oracle = dj_oracle_2q(grader1.dj_qubits, function)
                # build the qcirc
                circ = get_dj_circuit(user_oracle)

                counts = execute(circ, BACKEND, shots=1).result().get_counts()

                all_zeros = "0" * grader1.dj_qubits

                # if 00 has non zero prob, function is
                if all_zeros in counts:
                    user_func_type = "C"
                else:
                    user_func_type = "B"

            except:
                break

            if user_func_type == func_type:
                correct += 1
            else:
                break

        return correct == grader1.total_tests

    @classmethod
    def evaluate(cls, dj_oracle_2q):
        # get min swaps lines is the users' function

        # now, I will time the runner function

        # if it is within limits, it will be fine

        # update team
        cls.return_json["team-id"] = cls.get_team_id()
        tle = False

        try:
            with time_limit(grader1.time_limit):
                success = grader1.run(dj_oracle_2q)
        except:
            print("here")
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["4.1"]["done"] = success
        cls.return_json["problem"]["4.1"]["wrong"] = not success

        # post the json to server

        # request = requests.post(QBRAID_API, data=cls.return_json)

        print("JSON object is :", cls.return_json)
        # if request.ok:
        if success:
            print(CORRECT_STMT)
        else:
            if tle:
                print(TIME_STMT)
            else:
                print(WRONG_STMT)
        # else:
        #     print(SERVER_STMT)
        # wrong answer


class grader2:
    ip_task_path = INPUT_PATH + "task-2-"
    op_task_path = OUTPUT_PATH + "task-2-"
    dj_qubits = 4
    total_tests = 10
    time_limit = 20
    return_json = {
        "team-id": None,
        "problem": {"4.2": {"points": "75", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        pass

    @staticmethod
    def run(dj_oracle_4q):
        correct = 0

        # load your tests here
        for test in range(grader2.total_tests):
            ip_test_path = grader2.ip_task_path + str(test) + ".txt"
            func_type, function = test_loader_1(ip_test_path)
            try:
                user_oracle = dj_oracle_4q(grader2.dj_qubits, function)
                # build the qcirc
                circ = get_dj_circuit(user_oracle)

                counts = execute(circ, BACKEND, shots=1).result().get_counts()

                all_zeros = "0" * grader2.dj_qubits

                # if 00 has non zero prob, function is
                if all_zeros in counts:
                    user_func_type = "C"
                else:
                    user_func_type = "B"

            except:
                break

            if user_func_type == func_type:
                correct += 1
            else:
                break

        return correct == grader2.total_tests

    @classmethod
    def evaluate(cls, dj_oracle_4q):

        # if it is within limits, it will be fine

        # update team
        cls.return_json["team-id"] = cls.get_team_id()
        tle = False

        try:
            with time_limit(grader2.time_limit):
                success = grader2.run(dj_oracle_4q)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["4.2"]["done"] = success
        cls.return_json["problem"]["4.2"]["wrong"] = not success

        # post the json to server : to do

        # request = requests.post(QBRAID_API, data=cls.return_json)

        # if request.ok:
        if success:
            print(CORRECT_STMT)
        else:
            if tle:
                print(TIME_STMT)
            else:
                print(WRONG_STMT)
        # else:
        #     print(SERVER_STMT)
        # wrong answer


class grader3:
    # to do...

    ip_task_path = INPUT_PATH + "task-2-"
    op_task_path = OUTPUT_PATH + "task-2-"
    total_tests = 10
    time_limit = 60
    return_json = {
        "team-id": None,
        "problem": {"4.3": {"points": "125", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        pass

    @staticmethod
    def run(dj_function_distribution):
        correct = 0

        # load your tests here
        for test in range(grader3.total_tests):
            ip_test_path = grader3.ip_task_path + str(test) + ".txt"
            N, K, f_types, test_functions = test_loader_2(ip_test_path)
            try:
                user_oracle = dj_function_distribution(N, K, test_functions)
            except:
                break

        # to do...
        return correct == grader3.total_tests

    @classmethod
    def evaluate(cls, dj_function_distribution):

        # if it is within limits, it will be fine

        # update team
        cls.return_json["team-id"] = cls.get_team_id()
        tle = False

        try:
            with time_limit(grader3.time_limit):
                success = grader3.run(dj_function_distribution)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["4.3"]["done"] = success
        cls.return_json["problem"]["4.3"]["wrong"] = not success

        # post the json to server : to do

        # request = requests.post(QBRAID_API, data=cls.return_json)

        # if request.ok:
        if success:
            print(CORRECT_STMT)
        else:
            if tle:
                print(TIME_STMT)
            else:
                print(WRONG_STMT)
        # else:
        #     print(SERVER_STMT)
        # wrong answer
