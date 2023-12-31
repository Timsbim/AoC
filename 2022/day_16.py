# --------------------------------------------------------------------------- #
#    Day 16                                                                   #
# --------------------------------------------------------------------------- #

import multiprocessing as mp
import re
from itertools import combinations, product

DAY = 16
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_report(file_name):
    re_valve = re.compile(
        r"^Valve (\S+) has flow rate=(\d+); "
        "tunnels? leads? to valves? ([^$]+)$"
    )
    rates, tunnels = {}, {}
    with open(file_name, "r") as file:
        for line in file:
            valve, rate, to_valves = re_valve.match(line.rstrip()).groups()
            if rate != "0":
                rates[valve] = int(rate)
            tunnels[valve] = set(to_valves.split(", "))
    return tunnels, rates
            
# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def shortest_path_length_base(graph, src, dst, excluded=None):
    if excluded == None:
        excluded = set()
    n, paths = 0, [[src]]
    while paths:
        n += 1
        next_paths = []
        for path in paths:
            visited = excluded.union(path)
            for node in graph[path[-1]]:
                if node == dst:
                    return n
                if node in visited:
                    continue
                next_paths.append(path + [node])
        paths = next_paths
    return None


def shortest_path_length(graph, src, dst, dists=None, excluded=None):
    if dists is None:
        dists = {
            (n1, n2): 1 for n1, n2 in product(graph, repeat=2) if n1 != n2
        }
    if excluded is None:
        excluded = set()
    min_length, paths = float("inf"), [([src], 0)]
    while paths:
        next_paths = []
        for path, length in paths:
            visited = excluded.union(path)
            for next_node in graph[path[-1]]:
                next_length = length + dists[path[-1], next_node]
                if next_node == dst:
                    min_length = min(min_length, next_length)
                    continue
                if next_node in visited:
                    continue
                if next_length < min_length:
                    next_paths.append((path + [next_node], next_length))
        paths = next_paths
    return min_length if min_length is not float("inf") else None


def compress_tunnels(tunnels, rates, dists=None):
    graph, new_dists = {}, {}
    excluded = set(["AA"] + list(rates))
    for src, dst in combinations(["AA"] + list(rates), r=2):
        length = shortest_path_length(tunnels, src, dst, dists, excluded)
        if length is not None:
            graph.setdefault(src, []).append(dst)
            graph.setdefault(dst, []).append(src)
            new_dists[src, dst] = new_dists[dst, src] = length
    return graph, new_dists


def release_by_one(tunnels, dists, rates, max_count=30):
    paths, max_release = [(set(), "AA", {"AA": 0}, max_count, 0)], 0
    while paths:
        next_paths = []
        for opened, valve, visited, count, release in paths:
            closed = set(rates) - opened
            # 2 remaining minutes amount to no contribution
            if count <= 2 or len(closed) == 0:
                max_release = max(max_release, release)
                continue
            for next_valve in tunnels[valve]:
                dist = dists[valve, next_valve]
                # Too far away
                if dist >= count:
                    max_release = max(max_release, release)
                    continue
                # Idle loop is wasted time
                if next_valve in visited and visited[next_valve] == release:
                    max_release = max(max_release, release)
                    continue
                # Open a still closed valve
                if next_valve in closed:
                    next_release = release + (count - dist - 1) * rates[next_valve]
                    next_paths.append((
                        opened | {next_valve},
                        next_valve,
                        dict(visited, **{next_valve: next_release}),
                        count - dist - 1,
                        next_release
                    ))
                # Move on (a still closed valve stays closed)
                next_visited = dict(visited, **{next_valve: release})
                next_paths.append((
                    set(opened), next_valve, next_visited, count - dist, release
                ))
        paths = next_paths
    return max_release


def subset_combos(rates):
    for n in range(1, len(rates) // 2):
        for combo in combinations(rates, r=n):
            yield combo, tuple(rate for rate in rates if rate not in combo)
    done = set()
    if len(rates) % 2 == 0:
        for combo in combinations(rates, len(rates) // 2):
            if combo in done:
                continue
            complement = tuple(rate for rate in rates if rate not in combo)
            done.add(complement)
            yield combo, complement


def release_by_two(tunnels, dists, rates):
    max_release = 0
    for subsets in subset_combos(rates):
        release = 0
        for subrates in subsets:        
            subrates = {v: r for v, r in rates.items() if v in subrates}
            comptunnels, compdists = compress_tunnels(tunnels, subrates, dists) 
            release += release_by_one(comptunnels, compdists, subrates, 26)
        max_release = max(max_release, release)
        print(max_release)
    return max_release


def release_by_two_mp(tunnels, dists, rates, subsets):
    release = 0
    for subrates in subsets:        
        subrates = {v: r for v, r in rates.items() if v in subrates}
        comptunnels, compdists = compress_tunnels(tunnels, subrates, dists) 
        release += release_by_one(comptunnels, compdists, subrates, 26)
    return release


if __name__ == "__main__":
    
    # ---------------------------------------------------------------------- #
    #    Part 1                                                              #
    # ---------------------------------------------------------------------- #   
    print("Part 1: ", end="\n", flush=True)
    
    tunnels, rates = get_report(file_name)
    tunnels, dists = compress_tunnels(tunnels, rates)
    print(release_by_one(tunnels, dists, rates, 30))  # 1873

    # ----------------------------------------------------------------------- #
    #    Part 2                                                               #
    # ----------------------------------------------------------------------- #
    print("Part 2: ", end="\n", flush=True)
    
    tunnels, rates = get_report(file_name)
    tunnels, dists = compress_tunnels(tunnels, rates)
    print(len(rates))
    print(len(list(subset_combos(rates))))
    with mp.Pool() as pool:
        args = (
            (tunnels, dists, rates, subsets)
            for subsets in subset_combos(rates)
        )
        releases = pool.starmap(release_by_two_mp, args)
    print(max(releases))  # 2425
