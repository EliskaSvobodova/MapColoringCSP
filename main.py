from backtracking import color_bt
from bt_consistency import color_consistency
from bt_filtering import color_bt_filtering
from stats import Stats


def solve(solve_func, domain, dirname, n, e):
    stats = Stats(n, e, domain, dirname)
    solve_func(n, e, domain, stats)
    stats.visualize()


def choose_map():
    choices = ['australia', 'germany']
    print("What map do you want to solve?")
    print(f"You can choose from: {', '.join(choices)}")
    map_name = input("Choice: ")
    while map_name not in choices:
        print(f"Unknown map, please select from: {', '.join(choices)}")
        map_name = input("Choice: ")
    return map_name


if __name__ == '__main__':
    filename = choose_map()
    with open(f'maps/{filename}') as f:
        lines = [l[:-1] for l in f.readlines()]
    nodes = lines[0].split(' ')
    edges = [l.split(' ') for l in lines[1:]]
    edges = [(e[0], e[1]) for e in edges]
    domain = ['R', 'G', 'B']
    solve(color_bt, domain, f"{filename}_bt", nodes, edges)
    solve(color_bt_filtering, domain, f"{filename}_bt_filtering", nodes, edges)
    solve(color_consistency, domain, f"{filename}_consistency", nodes, edges)

