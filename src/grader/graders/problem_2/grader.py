# simple graph problem
import os
import signal
from contextlib import contextmanager

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


script_dir = os.path.dirname(__file__)
REL_INPUT_PATH = "./tests/inputs/"
REL_OUTPUT_PATH = "./tests/outputs/"
INPUT_PATH = os.path.join(script_dir, REL_INPUT_PATH)
OUTPUT_PATH = os.path.join(script_dir, REL_OUTPUT_PATH)

CORRECT_STMT = "Congratulations, your answer is correct!"
WRONG_STMT = "Uh-oh, that's not quite correct :("
SERVER_STMT = "The server couldn't process your request correctly at the moment, please try again in a while"
TIME_STMT = "Uh-oh, time limit exceeded for the problem :("

QBRAID_API = None


def test_loader(file_path):
    # make it faster ...
    with open(file_path, "r") as file:
        controls = []
        targets = []
        connectivity = {}
        for row_id, row in enumerate(file):

            # first row
            if row_id == 0:
                n, m = row.split()
                n, m = int(n), int(m)
                connectivity = {x: [] for x in range(1, n + 1)}
            # edge rows
            elif row_id >= 1 and row_id <= m:
                u, v = row.split()
                u, v = int(u), int(v)

                # add edge
                connectivity[u].append(v)
                connectivity[v].append(u)

            # query row
            elif row_id == m + 1:
                continue  # queries row
            else:
                control, target = row.split()
                control, target = int(control), int(target)

                controls.append(control)
                targets.append(target)

    return n, m, controls, targets, connectivity


class grader1:
    ip_task_path = INPUT_PATH + "task-1-"
    op_task_path = OUTPUT_PATH + "task-1-"
    total_tests = 10
    time_limit = 10

    return_json = {
        "team-id": None,
        "problem": {"2.1": {"points": "30", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(get_min_swaps_line):

        correct = 0

        # load your tests here
        for test in range(grader1.total_tests):
            ip_test_path = grader1.ip_task_path + str(test) + ".txt"
            n, m, controls, targets, connectivity = test_loader(ip_test_path)
            try:
                user_min_swaps = get_min_swaps_line(n, controls, targets, connectivity)
            except:
                break
            # if there min swaps match with ours, they're good to go
            op_test_path = grader1.op_task_path + str(test) + ".txt"

            actual_swaps = [
                int(x) for x in open(op_test_path, "r").readlines()[0].split()
            ]

            if actual_swaps == user_min_swaps:
                correct += 1
            else:
                break

        return correct == grader1.total_tests

    @classmethod
    def evaluate(cls, get_min_swaps_line):
        # get min swaps lines is the users' function

        # now, I will time the runner function

        # if it is within limits, it will be fine

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
                success = grader1.run(get_min_swaps_line)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["2.1"]["done"] = success
        cls.return_json["problem"]["2.1"]["wrong"] = not success

        # post the json to server

        append_values(
            [
                cls.return_json["team-id"],
                "2.1",
                cls.return_json["problem"]["2.1"]["points"],
                cls.return_json["problem"]["2.1"]["done"],
                cls.return_json["problem"]["2.1"]["wrong"],
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
    ip_task_path = INPUT_PATH + "task-2-"
    op_task_path = OUTPUT_PATH + "task-2-"
    total_tests = 10
    time_limit = 60
    return_json = {
        "team-id": None,
        "problem": {"2.2": {"points": "70", "done": False, "wrong": False}},
    }

    @classmethod
    def get_team_id(cls):
        value = os.getenv("TEAMID", "Please enter your TEAMID")
        return value

    @staticmethod
    def run(get_min_swaps_graph):
        correct = 0

        # load your tests here
        for test in range(grader2.total_tests):
            ip_test_path = grader2.ip_task_path + str(test) + ".txt"
            n, m, controls, targets, connectivity = test_loader(ip_test_path)
            try:
                user_min_swaps = get_min_swaps_graph(
                    n, m, controls, targets, connectivity
                )
            except:
                break
            # if there min swaps match with ours, they're good to go
            op_test_path = grader2.op_task_path + str(test) + ".txt"

            actual_swaps = [
                int(x) for x in open(op_test_path, "r").readlines()[0].split()
            ]

            if actual_swaps == user_min_swaps:
                correct += 1
            else:
                print("Failed on ", ip_test_path)
                break

        return correct == grader2.total_tests

    @classmethod
    def evaluate(cls, get_min_swaps_line):

        # if it is within limits, it will be fine

        # update team
        if "TEAMID" in os.environ:
            cls.return_json["team-id"] = cls.get_team_id()
        else:
            cls.return_json["team-id"] = "NO TEAMID"
            print("Please add your TEAMID as an env variable")
            return

        tle = False

        try:
            with time_limit(grader2.time_limit):
                success = grader2.run(get_min_swaps_line)
        except:
            success = False
            tle = True

        # update json
        cls.return_json["problem"]["2.2"]["done"] = success
        cls.return_json["problem"]["2.2"]["wrong"] = not success

        # post the json to server : to do

        append_values(
            [
                cls.return_json["team-id"],
                "2.2",
                cls.return_json["problem"]["2.2"]["points"],
                cls.return_json["problem"]["2.2"]["done"],
                cls.return_json["problem"]["2.2"]["wrong"],
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
