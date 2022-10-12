import os

import signal
from contextlib import contextmanager
from qiskit import execute, QuantumCircuit, Aer
import numpy as np
from .answer import get_bell, get_even_odd
from ..google_sheets import append_values

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


CORRECT_STMT = "Congratulations, your answer is correct!"
WRONG_STMT = "Uh-oh, that's not quite correct :("
SERVER_STMT = "The server couldn't process your request correctly at the moment, please try again in a while"
TIME_STMT = "Uh-oh, time limit exceeded for the problem :("

QBRAID_API = None
SV_BACKEND = Aer.get_backend("statevector_simulator")


class grader1:

    time_limit = 10

    return_json = {
        "team-id": None,
        "problem": {"1.1": {"points": "10", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(make_bell):

        correct = False

        try:
            user_circuit = make_bell()

            # build the qcirc
            user_statevector = (
                execute(user_circuit, SV_BACKEND).result().get_statevector()
            )

            expected_circuit = get_bell()

            expected_statevector = (
                execute(expected_circuit, SV_BACKEND).result().get_statevector()
            )

            # if doubt solved, fine

            # op_test_path = grader1.op_task_path + str(test) + ".qpy"
            # expected_statevector = output_vector_loader(op_test_path)
        except:
            return False

        if user_statevector == expected_statevector:
            correct = True

        return correct

    @classmethod
    def evaluate(cls, make_bell):
        # update team
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return

        tle = False

        try:
            with time_limit(grader1.time_limit):
                success = grader1.run(make_bell)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["1.1"]["done"] = success
        cls.return_json["problem"]["1.1"]["wrong"] = not success

        # post the json to server
        append_values(
            [
                cls.return_json["team-id"],
                "1.1",
                cls.return_json["problem"]["1.1"]["points"],
                cls.return_json["problem"]["1.1"]["done"],
                cls.return_json["problem"]["1.1"]["wrong"],
            ]
        )

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
    total_tests = 10
    time_limit = 10
    return_json = {
        "team-id": None,
        "problem": {"1.2": {"points": "15", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(equal_superposition):

        correct = 0
        # load your tests here
        for test in range(grader2.total_tests):

            n = np.random.randint(2, 13)
            try:
                user_circuit = equal_superposition(n)

                # build the qcirc
                user_statevector = (
                    execute(user_circuit, SV_BACKEND).result().get_statevector()
                )

                expected_circuit = QuantumCircuit(n)
                expected_circuit.h(range(n))

                expected_statevector = (
                    execute(expected_circuit, SV_BACKEND).result().get_statevector()
                )

            except:
                break
            if user_statevector == expected_statevector:
                correct += 1
            else:
                break

        return correct == grader2.total_tests

    @classmethod
    def evaluate(cls, make_superposition):

        # update team
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return
        tle = False
        success = False
        try:
            with time_limit(grader2.time_limit):
                success = grader2.run(make_superposition)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["1.2"]["done"] = success
        cls.return_json["problem"]["1.2"]["wrong"] = not success

        # post the json to server : to do

        append_values(
            [
                cls.return_json["team-id"],
                "1.2",
                cls.return_json["problem"]["1.2"]["points"],
                cls.return_json["problem"]["1.2"]["done"],
                cls.return_json["problem"]["1.2"]["wrong"],
            ]
        )

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
    total_tests = 10
    time_limit = 20
    return_json = {
        "team-id": None,
        "problem": {"1.3": {"points": "25", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(make_even_odd):

        correct = 0
        # load your tests here
        for test in range(grader3.total_tests):
            n = np.random.randint(2, 13)
            try:
                user_even, user_odd = make_even_odd(n)

                # build the qcirc
                user_even_statevector = (
                    execute(user_even, SV_BACKEND).result().get_statevector()
                )

                user_odd_statevector = (
                    execute(user_odd, SV_BACKEND).result().get_statevector()
                )

                expected_even_statevector, expected_odd_statevector = get_even_odd(n)

            except:
                break
            condition1 = user_even_statevector == expected_even_statevector
            condition2 = user_odd_statevector == expected_odd_statevector
            if condition1 and condition2:
                correct += 1
            else:
                break

        return correct == grader3.total_tests

    @classmethod
    def evaluate(cls, make_even_odd):
        # update team
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return
        tle = False

        try:
            with time_limit(grader3.time_limit):
                success = grader3.run(make_even_odd)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["1.3"]["done"] = success
        cls.return_json["problem"]["1.3"]["wrong"] = not success

        # post the json to server : to do

        append_values(
            [
                cls.return_json["team-id"],
                "1.3",
                cls.return_json["problem"]["1.3"]["points"],
                cls.return_json["problem"]["1.3"]["done"],
                cls.return_json["problem"]["1.3"]["wrong"],
            ]
        )
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
