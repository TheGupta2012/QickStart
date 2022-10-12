# simple graph problem
import os
import signal
from contextlib import contextmanager
from qiskit import execute, QuantumCircuit, Aer
import numpy as np

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
BACKEND = Aer.get_backend("qasm_simulator")


def get_random_choice():
    choices = ["balanced", "constant"]

    return np.random.choice(choices, 1)


def dj_oracle(case, n):
    # We need to make a QuantumCircuit object to return
    # This circuit has n+1 qubits: the size of the input,
    # plus one output qubit
    oracle_qc = QuantumCircuit(n + 1)

    if case == "balanced":

        b = np.random.randint(1, 2**n)

        # Next, format 'b' as a binary string of length 'n', padded with zeros:
        b_str = format(b, "0" + str(n) + "b")

        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

        # Do the controlled-NOT gates for each qubit, using the output qubit
        # as the target:

        for qubit in range(n):
            oracle_qc.cx(qubit, n)

        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

    if case == "constant":
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)

        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)

    oracle_gate = oracle_qc
    oracle_gate.name = "Oracle"  # To show when we display the circuit

    return oracle_gate


class grader1:

    dj_qubits = 2
    total_tests = 7
    time_limit = 20

    return_json = {
        "team-id": None,
        "problem": {"4.1": {"points": "50", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(dj_circuit_2q):

        correct = 0
        # load your tests here
        for _ in range(grader1.total_tests):

            func_type = get_random_choice()[0]
            random_oracle = dj_oracle(func_type, 2)

            try:
                # build the qcirc
                circ = dj_circuit_2q(random_oracle)
                counts = execute(circ, BACKEND, shots=1).result().get_counts()

                all_zeros = "0" * grader1.dj_qubits

                # if 00 has non zero prob, function is constant
                if all_zeros in counts:
                    user_func_type = "constant"
                else:
                    user_func_type = "balanced"

            except:
                break

            if user_func_type == func_type:
                correct += 1
            else:
                break

        return correct == grader1.total_tests

    @classmethod
    def evaluate(cls, dj_circuit_2q):
        # get min swaps lines is the users' function

        # now, I will time the runner function

        # if it is within limits, it will be fine

        # update team
        if 'TEAMID' in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable") 
        tle = False

        try:
            with time_limit(grader1.time_limit):
                success = grader1.run(dj_circuit_2q)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["4.1"]["done"] = success
        cls.return_json["problem"]["4.1"]["wrong"] = not success

        # post the json to server

        append_values([cls.return_json["team-id"],"4.1",cls.return_json["problem"]["4.1"]["points"],cls.return_json["problem"]["4.1"]["done"],cls.return_json["problem"]["4.1"]["wrong"]])

        # print("JSON object is :", cls.return_json)
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
    dj_qubits = 4
    total_tests = 10
    time_limit = 20
    return_json = {
        "team-id": None,
        "problem": {"4.2": {"points": "75", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(dj_circuit_4q):

        correct = 0
        # load your tests here
        for _ in range(grader2.total_tests):

            func_type = get_random_choice()[0]
            random_oracle = dj_oracle(func_type, 4)
            try:
                # build the qcirc
                circ = dj_circuit_4q(random_oracle)
                counts = execute(circ, BACKEND, shots=1).result().get_counts()

                all_zeros = "0" * grader2.dj_qubits

                # if 00 has non zero prob, function is constant
                if all_zeros in counts:
                    user_func_type = "constant"
                else:
                    user_func_type = "balanced"

            except:
                break

            if user_func_type == func_type:
                correct += 1
            else:
                break

        return correct == grader2.total_tests

    @classmethod
    def evaluate(cls, dj_circuit_4q):

        # if it is within limits, it will be fine

        # update team
        if 'TEAMID' in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable") 
        tle = False

        try:
            with time_limit(grader2.time_limit):
                success = grader2.run(dj_circuit_4q)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["4.2"]["done"] = success
        cls.return_json["problem"]["4.2"]["wrong"] = not success

        # post the json to server : to do

        append_values([cls.return_json["team-id"],"4.2",cls.return_json["problem"]["4.2"]["points"],cls.return_json["problem"]["4.2"]["done"],cls.return_json["problem"]["4.2"]["wrong"]])

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
        "problem": {"4.3": {"points": "125", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        pass

    @staticmethod
    def run(dj_circuit_general):

        correct = 0
        # load your tests here
        for _ in range(grader3.total_tests):

            func_type = get_random_choice()[0]
            n = np.random.randint(2, 11)
            random_oracle = dj_oracle(func_type, n)
            try:
                # build the qcirc

                circ = dj_circuit_general(n, random_oracle)

                counts = execute(circ, BACKEND, shots=1).result().get_counts()

                all_zeros = "0" * n  # for this test

                # if 00 has non zero prob, function is constant
                if all_zeros in counts:
                    user_func_type = "constant"
                else:
                    user_func_type = "balanced"

            except:
                break

            if user_func_type == func_type:
                correct += 1
            else:
                break

        return correct == grader3.total_tests

    @classmethod
    def evaluate(cls, dj_circuit_general):

        # if it is within limits, it will be fine

        # update team
        if 'TEAMID' in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable") 
        tle = False

        try:
            with time_limit(grader3.time_limit):
                success = grader3.run(dj_circuit_general)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["4.3"]["done"] = success
        cls.return_json["problem"]["4.3"]["wrong"] = not success

        # post the json to server : to do

        append_values([cls.return_json["team-id"],"4.2",cls.return_json["problem"]["4.2"]["points"],cls.return_json["problem"]["4.2"]["done"],cls.return_json["problem"]["4.2"]["wrong"]])


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
