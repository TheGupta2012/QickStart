import json

# will help tp keep this in the server for each team
def get_init_team_json(team_id):
    challenge = json.load(open("problem-structure.json", "r"))
    team_json = {"team-id": str(team_id)}

    # problem dict
    problems = dict()
    points = {
        1: {1: 10, 2: 20, 3: 20},
        2: {1: 30, 2: 70},
        3: {1: 40, 2: 60, 3: 100},
        4: {1: 50, 2: 75, 3: 125},
        5: {1: 75, 2: 125, 3: 200},
    }

    for problem in challenge["problem-structure"]:
        num = int(problem)
        tasks = int(challenge["problem-structure"][problem])
        problem_dict = {}
        for task in range(1, tasks + 1):
            point = points[num][task]
            problem_init = {"wrong-count": "0", "points": str(point), "done": False}
            problem_dict[str(task)] = problem_init

        problems[problem] = problem_dict

    team_json["problems"] = problems

    json.dump(team_json, open("team-json-template.json", "w"))
    return team_json


print(get_init_team_json(123))
