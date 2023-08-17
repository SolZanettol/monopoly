import random
import importlib
simulator = importlib.import_module("monopoly-simulator")


def heuristic():
    games = parse_input()

    # TODO ajouter votre heuristique ici. L'utilisation de la fonction parse_input est facultative
    heuristic_results = [500 for game in games]

    with open("out.txt", 'w') as f:
        f.writelines([str(result) + '\n' for result in heuristic_results])


def parse_input():
    with open("in.txt", 'r') as f:
        lines = f.readlines()
    games = []
    for i in range(32, len(lines) + 1, 32):
        spaces = [{
            "space_number": fields[0],
            "space_name": fields[1],
            "n_houses": fields[2],
            "is_mortgaged": fields[3],
            "owned_by": fields[4] if len(fields) > 4 else None
        } for fields in [l.replace('\n', '').split(' ') for l in lines[i - 32:i - 4]]]
        players = [{
            "player_name": fields[0],
            "money": fields[1],
            "space": fields[2]
        } for fields in [l.replace('\n', '').split(' ') for l in lines[i - 4:i]]]

        games += [{"spaces": spaces, "players": players}]
    return games

def test_heuristic(overwrite_in=True):
    if overwrite_in:
        random.seed()
        amounts = [random.randint(500, 2500) for _ in range(1000)]
        simulator.run_simulation(parallel=False, amounts=amounts, n_sim=1000)
    else:
        with open("amounts.txt", 'r') as f:
            amounts = [int(l.replace('\n', '')) for l in f.readlines()]


    heuristic()

    with open("out.txt", 'r') as f:
        lines = f.readlines()


    penalties = []
    for real, estimate in zip(amounts, lines):
        if int(estimate) <= real:
            penalties += [real - int(estimate)]
        else:
            penalties += [100000]

    print("Penalties:")
    for p in penalties:
        print(p)
    print("Total penalties:")
    print(sum(penalties))


if __name__ == "__main__":
    test_heuristic(overwrite_in=True)
