# --------------------------------------------------------------------------- #
#     Moving files to 2021 folder                                             #
# --------------------------------------------------------------------------- #

import re
from pathlib import Path

DAY = 17

path = Path()
hist_path = path / "2021"
hist_path.mkdir(exist_ok=True)

re_day = re.compile(r"_(\d\d)")
for file_path in path.glob("day_*.*"):
    day = re_day.search(file_path.name).group(1)
    if int(day) < DAY:
        file_path.rename(hist_path / file_path.name)

# --------------------------------------------------------------------------- #
#     Renaming files                                                          #
# --------------------------------------------------------------------------- #

import re
from pathlib import Path

re_split = re.compile(r"_|\.")
path = Path()
for file_path in path.glob("*.csv"):
    day, *example = re_split.split(file_path.name)[1:-1]
    example = "_example" if example else ""
    file_path.rename(f"day_{day}_input{example}.csv")


def repl(match):
    day, example = match.groups()
    example = "_example" if example else ""
    return f"day_{day}_input{example}.csv"


re_file = re.compile(r"input_(\d\d)(.*?)\.csv")
path = Path()
for file_path in path.glob("*.py"):
    if file_path.name == "current.py":
        continue
    with open(file_path, "r") as file:
        file_str = file.read()
    with open(file_path, "w") as file:
        file.write(re_file.sub(repl, file_str))


# --------------------------------------------------------------------------- #
#     Inserting section seperators                                            #
# --------------------------------------------------------------------------- #

import re

re_section_head = re.compile(
    r"""
        ^[ ]*\#[ ]*
        (
            Day\s+\d\d
            | Preparation
            | Reading\s+input
            | Helper\s+functions
            | Part\s+\d
        )
        [ ]*$
    """,
    re.VERBOSE|re.MULTILINE
)

re_seperator = re.compile(
    r"^[ ]*#[ ]*-+$\n",
    re.MULTILINE
)


def repl(match):
    sep = "# " + "-" * 75 + " #"
    return (
        sep + "\n"
        + "#" + " " * 4 + match[1] + " " * (72 - len(match[1])) + " #\n"
        + sep
    )

with open("current.py", "r") as file:
    code = file.read()
code = re_seperator.sub("", code)
code = re_section_head.sub(repl, code)
with open("current.py", "w") as file:
    file.write(code)
