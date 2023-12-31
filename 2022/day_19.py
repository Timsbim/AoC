# --------------------------------------------------------------------------- #
#    Day 19                                                                   #
# --------------------------------------------------------------------------- #

import re
import multiprocessing as mp
from functools import partial

DAY = 19
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_blueprints(file_name):
    re_blueprint = re.compile(
        "Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot "
        "costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. "
        "Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    blueprints = []
    with open(file_name, "r") as file:
        for line in file:
            blueprint = {}
            costs = [*map(int, re_blueprint.match(line).groups())]
            blueprint["ore"] = {"ore": costs[0]}
            blueprint["clay"] = {"ore": costs[1]}
            blueprint["obsidian"] = {"ore": costs[2], "clay": costs[3]}
            blueprint["geode"] = {"ore": costs[4], "obsidian": costs[5]}
            blueprint["max_ores"] = max(costs[:3] + [costs[4]])
            blueprint["max_clays"] = blueprint["obsidian"]["clay"]
            blueprint["max_obsidians"] = blueprint["geode"]["obsidian"]
            blueprints.append(blueprint)
    return blueprints

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def factories(blueprint, robots, minerals):
    ore, clay, obsidians, geodes = minerals
    ore_robots, clay_robots, obsidian_robots, geode_robots = robots
    # If possible build a geode robot
    costs = blueprint["geode"]
    if ore >= costs["ore"] and obsidians >= costs["obsidian"]:
        return [(
            (ore_robots, clay_robots, obsidian_robots, geode_robots + 1),
            (ore - costs["ore"], clay, obsidians - costs["obsidian"], geodes)
        )]
    # Next best option: build an obsidian robot, if needed
    deltas = []
    if obsidian_robots < blueprint["max_obsidians"]:
        costs = blueprint["obsidian"]
        if ore >= costs["ore"] and clay >= costs["clay"]:
            deltas.append((
                (ore_robots, clay_robots, obsidian_robots + 1, geode_robots),
                (ore - costs["ore"], clay - costs["clay"], obsidians, geodes)
            ))
    if ore_robots < blueprint["max_ores"]:
        costs = blueprint["ore"]
        if ore >= costs["ore"]:
            deltas.append((
                (ore_robots + 1, clay_robots, obsidian_robots, geode_robots),
                (ore - costs["ore"], clay, obsidians, geodes)
            ))
    if clay_robots < blueprint["max_clays"]:
        costs = blueprint["clay"]
        if ore >= costs["ore"]:
            deltas.append((
                (ore_robots, clay_robots + 1, obsidian_robots, geode_robots),
                (ore - costs["ore"], clay, obsidians, geodes)
            ))
    if ore_robots < blueprint["max_ores"]:
        deltas.append((robots, minerals))
    return deltas


def only_new_geode_robots(blueprint, robots):
    ore_robots, clay_robots, obsidian_robots = robots[:3]
    return (
        ore_robots == blueprint["max_ores"]
        and clay_robots == blueprint["max_clays"]
        and obsidian_robots == blueprint["max_obsidians"]
    )


def max_geodes(ID, blueprint, minutes=24, show=True):
    factory = partial(factories, blueprint)
    # Start with one ore robot after 2 minutes, i.e. 2 ore
    paths = {((1, 0, 0, 0), (2, 0, 0, 0))}
    visited = {((1, 0, 0, 0), (2, 0, 0, 0))}
    for minute in range(3, minutes):
        next_paths = set()
        max_geodes = []
        for robots, minerals in paths:
            for next_robots, next_minerals in factory(robots, minerals):
                next_minerals = (m + r for m, r in zip(next_minerals, robots))
                next_minerals = tuple(next_minerals)
                if (next_robots, next_minerals) not in visited:
                    next_paths.add((next_robots, next_minerals))
                    visited.add((next_robots, next_minerals))
        paths = next_paths     
        max_geodes.append(max(minerals[-1] for _, minerals in paths))
    # No need to build robots during the last round
    max_geodes = max(minerals[-1] + robots[-1] for robots, minerals in paths)
    if show:
        print(f"ID: {ID} -> {max_geodes} geodes")
    return max_geodes


if __name__ == "__main__":
    print("Day", DAY)

    # ----------------------------------------------------------------------- #
    #    Part 1                                                               #
    # ----------------------------------------------------------------------- #
    print("Part 1: ", end="")
    args = enumerate(get_blueprints(file_name), 1)
    with mp.Pool() as pool:
        levels = pool.starmap(max_geodes, args)
    print(sum(ID * level for ID, level in enumerate(levels, 1)))  # 1653
    
    # ----------------------------------------------------------------------- #
    #    Part 2                                                               #
    # ----------------------------------------------------------------------- #
    print("Part 2: ", end="\n")
    
    args = (
        (ID, blueprint, 32)
        for ID, blueprint in enumerate(get_blueprints(file_name)[:3], 1)
    )
    with mp.Pool() as pool:
        levels = pool.starmap(max_geodes, args)
    print(levels)
    print(levels[0] * levels[1] * levels[2])  # 4212
