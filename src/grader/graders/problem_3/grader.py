import os

from qiskit import execute, QuantumCircuit
import signal
from contextlib import contextmanager
from qiskit import Aer
from math import pi

from ..google_sheets import append_values


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


# some global values
PI_2 = pi / 2

INPUT_PATH = "./tests/inputs/"
OUTPUT_PATH = "./tests/outputs/"

CORRECT_STMT = "Congratulations, your answer is correct!"
WRONG_STMT = "Uh-oh, that's not quite correct :("
SERVER_STMT = "The server couldn't process your request correctly at the moment, please try again in a while"
TIME_STMT = "Uh-oh, time limit exceeded for the problem :("

QBRAID_API = None
BACKEND = Aer.get_backend("qasm_simulator")

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


def test_loader_1(file_path):
    # make it faster ...
    arz, arx, ary = [], [], []

    with open(file_path, "r") as file:
        for row_id, row in enumerate(file):
            if row_id == 0:
                state = row[0]
            else:
                elements = [int(x) for x in row[:-1].split(",")]
                if row_id == 1:
                    arz = elements
                elif row_id == 2:
                    arx = elements
                else:
                    ary = elements

    return state, arz, arx, ary


class grader1:
    state_set = {"0", "1", "-", "+", "r", "l"}

    time_limit = 5

    return_json = {
        "team-id": None,
        "problem": {"3.1": {"points": "40", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(generate_bloch_operation):
        correct = 0
        for state in grader1.state_set:
            # user code
            try:
                rotations = generate_bloch_operation(state)

                # execute and check
                circuit = get_circuit(state, rotations[0], rotations[1], rotations[2])
                result = execute(circuit, BACKEND).result()
                counts = result.get_counts()

            except:
                break
            # correct circuit if only 0 present
            if len(counts) == 1 and "0" in counts.keys():
                correct += 1
            else:
                break

        return correct == len(grader1.state_set)

    @classmethod
    def evaluate(cls, generate_bloch_operation):
        # we will evaluate it on different states
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return

        tle = False

        try:
            with time_limit(grader1.time_limit):
                success = grader1.run(generate_bloch_operation)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["3.1"]["done"] = success
        cls.return_json["problem"]["3.1"]["wrong"] = not success

        # post to the sheet
        append_values(
            [
                cls.return_json["team-id"],
                "3.1",
                cls.return_json["problem"]["3.1"]["points"],
                cls.return_json["problem"]["3.1"]["done"],
                cls.return_json["problem"]["3.1"]["wrong"],
            ]
        )

        if success:
            print(CORRECT_STMT)
        else:
            if tle:
                print(TIME_STMT)
            else:
                print(WRONG_STMT)


class grader2:
    state_set = {"0", "1", "-", "+", "r", "l"}
    ip_task_path = INPUT_PATH + "task-2-"
    op_task_path = OUTPUT_PATH + "task-2-"
    total_tests = 10
    time_limit = 20

    return_json = {
        "team-id": None,
        "problem": {"3.2": {"points": "60", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(get_total_bloch_ops):
        # run the tests
        correct = 0

        for test in range(10):
            ip_test_path = grader2.ip_task_path + str(test) + ".txt"

            state, arz, arx, ary = test_loader_1(ip_test_path)

            user_total = get_total_bloch_ops(state, arz, arx, ary)

            # read the bloch ops from the outputs

            op_test_path = grader2.op_task_path + str(test) + ".txt"

            expected_total = int(open(op_test_path).readlines()[0])

            if user_total == expected_total:
                correct += 1
            else:
                break

        return correct == grader2.total_tests

    @classmethod
    def evaluate(cls, get_total_bloch_ops):
        # we will evaluate it on different states
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return

        tle = False

        try:
            with time_limit(grader2.time_limit):
                success = grader2.run(get_total_bloch_ops)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["3.2"]["done"] = success
        cls.return_json["problem"]["3.2"]["wrong"] = not success

        # post to the sheet
        append_values(
            [
                cls.return_json["team-id"],
                "3.2",
                cls.return_json["problem"]["3.2"]["points"],
                cls.return_json["problem"]["3.2"]["done"],
                cls.return_json["problem"]["3.2"]["wrong"],
            ]
        )

        if success:
            print(CORRECT_STMT)
        else:
            if tle:
                print(TIME_STMT)
            else:
                print(WRONG_STMT)


class grader3:
    ip_task_path = INPUT_PATH + "task-3-"
    op_task_path = OUTPUT_PATH + "task-3-"
    total_tests = 10
    time_limit = 10

    return_json = {
        "team-id": None,
        "problem": {"3.3": {"points": "100", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(get_larger_total_bloch_ops):
        # run the tests
        correct = 0

        for test in range(10):
            ip_test_path = grader3.ip_task_path + str(test) + ".txt"

            state, arz, arx, ary = test_loader_1(ip_test_path)

            user_total = get_larger_total_bloch_ops(state, arz, arx, ary)

            # read the bloch ops from the outputs

            op_test_path = grader3.op_task_path + str(test) + ".txt"

            expected_total = int(open(op_test_path).readlines()[0])

            if user_total == expected_total:
                correct += 1
            else:
                break

        return correct == grader3.total_tests

    @classmethod
    def evaluate(cls, get_larger_total_bloch_ops):
        # we will evaluate it on different states
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return

        tle = False

        try:
            with time_limit(grader3.time_limit):
                success = grader3.run(get_larger_total_bloch_ops)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["3.3"]["done"] = success
        cls.return_json["problem"]["3.3"]["wrong"] = not success

        # post to the sheet
        append_values(
            [
                cls.return_json["team-id"],
                "3.3",
                cls.return_json["problem"]["3.3"]["points"],
                cls.return_json["problem"]["3.3"]["done"],
                cls.return_json["problem"]["3.3"]["wrong"],
            ]
        )

        if success:
            print(CORRECT_STMT)
        else:
            if tle:
                print(TIME_STMT)
            else:
                print(WRONG_STMT)
