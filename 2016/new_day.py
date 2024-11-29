import sys
from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent


YEAR = 2016


parser = ArgumentParser()
parser.add_argument("day", type=int)
day = parser.parse_args().day


if day < 1 or 25 < day:
    print(f"Error: day {day} not in range!")
    sys.exit(1)

day_str = f"{day:0>2}"

path = Path(f"{YEAR}/day_{day_str}_input_example.txt")
if path.exists():
    print(f"File '{str(path)}' already exists!")
else:
    path.touch()

path = Path(f"{YEAR}/day_{day_str}_input.txt")
if path.exists():
    print(f"File '{str(path)}' already exists!")
else:
    path.touch()

path = Path(f"{YEAR}/day_{day_str}.py")
if path.exists():
    print(f"File '{str(path)}' already exists!")
    sys.exit()

sep = "# " + (79 - 4) * "-" + " #\n"
mid = f"#    Day {day}"
mid = mid + (79 - len(mid) - 1) * " " + "#\n"
content = sep + mid + sep
content += dedent(f"""\
    from pprint import pprint


    DAY = {day}
    EXAMPLE = True

    # --------------------------------------------------------------------------- #
    #    Preparation                                                              #
    # --------------------------------------------------------------------------- #
    print("Day", DAY)

    file_name = f"2016/day_{{DAY:0>2}}_input"
    if EXAMPLE:
        file_name += "_example"
    file_name += ".txt"

    # --------------------------------------------------------------------------- #
    #    Reading input                                                            #
    # --------------------------------------------------------------------------- #

    with open(file_name, "r") as file:
        pass
    if EXAMPLE:
        #pprint()
        pass

    # --------------------------------------------------------------------------- #
    #    Helper                                                                   #
    # --------------------------------------------------------------------------- #



    # --------------------------------------------------------------------------- #
    #    Part 1                                                                   #
    # --------------------------------------------------------------------------- #
    print("Part 1: ", end="")


    def part_1():
        return None


    print(solution := part_1())
    # assert solution == (if EXAMPLE else)

    # --------------------------------------------------------------------------- #
    #    Part 2                                                                   #
    # --------------------------------------------------------------------------- #
    print("Part 2: ", end="")


    def part_2():
        return None


    print(solution := part_2())
    # assert solution == (if EXAMPLE else)
    """)
path.write_text(content)
