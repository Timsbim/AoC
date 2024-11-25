import re
from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent


def get_argument():
    """ Only one required argument: The last day """
    parser = ArgumentParser()
    parser.add_argument("day", type=int)
    args = parser.parse_args()
    return args.day


def override(filename):
    while True:
        answer = input(f"Override `{filename}` [Y/N]? ").strip()
        if not answer or answer[0].lower() not in {"y", "n"}:
            print(f"'{answer}' is not a valid answer!")
            continue
        answer = answer[0].lower()
        return True if answer == "y" else False


def archive_files(day, year=2023):
    """ Move all the files for days less or equal to the given to archive
    folder
    """
    path = Path()
    hist_path = path / str(year)
    hist_path.mkdir(exist_ok=True)

    # Creating the `day_n.py` file if it doesn't exist
    daypy_path = Path(f"day_{day:0>2}.py")
    currentpy_path = Path("current.py")
    if not daypy_path.exists() and currentpy_path.exists():
        print(f"Creating '{daypy_path}' ...")
        content = currentpy_path.read_text()
        pattern = '^file_name = f"day_{DAY:0>2}_input"$'
        if match := re.search(pattern, content, flags=re.M):
            start, end = match.span()
            repl = f'file_name = f"{year}/day_{{DAY:0>2}}_input"'
            content = content[:start] + repl + content[end:]
        daypy_path.write_text(content)

    # Moving the files
    re_day = re.compile(r"_(\d\d)")
    for file_path in path.glob("day_*.*"):
        day_str = re_day.search(file_path.name).group(1)
        if int(day_str) <= day:
            hist_file_path = hist_path / file_path.name
            move = True
            if hist_file_path.exists() and not override(str(hist_file_path)):
                move = False
            if move:
                print(f"Moving '{file_path}' to '{hist_file_path}'...")
                file_path.rename(hist_file_path)
    

SEP_LINE = "# " + "-" * 75 + " #\n"
DAY_LINE = "#    Day "
CODE_BLOCK = dedent('''\
EXAMPLE = True

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    #for line in file:
    pass

if EXAMPLE:
    #pprint()
    pass

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #



# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return None


solution = part_1()
#assert solution == (if EXAMPLE else)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


solution = part_2()
#assert solution == (if EXAMPLE else)
print(solution)

''')


def write_new_blank_files(day):
    """ Write new `current.py`, `day_n_input.txt` and `day_n_input_example.txt`
    files for the next day
    """

    # Python file
    print("Creating new 'current.py' ...")
    current_str = SEP_LINE
    next_day = str(day + 1)
    current_str += (DAY_LINE + next_day + " " * (68 - len(next_day)) + " #\n")
    current_str += SEP_LINE + "from pprint import pprint\n\n\n"
    current_str += "DAY = " + next_day + "\n"
    current_str += CODE_BLOCK
    with open("current.py", "w") as file:
        file.write(current_str)

    # Input files
    next_day = day + 1
    print(f"Creating 'day_{next_day:0>2}_input.txt' ...")
    Path(f"day_{next_day:0>2}_input.txt").touch()
    print(f"Creating 'day_{next_day:0>2}_input_example.txt' ...")
    Path(f"day_{next_day:0>2}_input_example.txt").touch()    


if __name__ == "__main__":

    day = get_argument()
    archive_files(day)
    write_new_blank_files(day)
