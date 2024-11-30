import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from shutil import move


# Get argument: year to process
parser = ArgumentParser()
parser.add_argument("year", type=int)
year = parser.parse_args().year
if year < 2015 or 2024 < year:
    print(f"Error: year {year} not in range!")
    sys.exit(1)
year = str(year)


# Moving the input files to new input subfolder
path = Path(f"/home/runner/AoC/{year}/")

# Create input subpath
path_input = path / "input"
path_input.mkdir(exist_ok=True)

# Move input files into the new folder
print("Moving input files ...")
for file in path.glob("day_[0-2][0-9]_input*.*"):
    print("  ", file)
    move(file, path_input / file.name.replace("_input", ""))
print("... finished")


# Replace file path for input files in Python files
print("Modifying Python files ...")
pattern = re.compile(
    f"({year}/)(day_[0-2]\d)_input((?:_example)?.(?:csv|txt))"
)
def repl(m): return f"{m[1]}input/{m[2]}{m[3]}"
for file_path in path.glob("day_[0-2][0-9].py"):
    with open(file_path, 'r') as file:
        code = file.read()
    if pattern.search(code):
        print(" ", file_path)
        code = pattern.sub(repl, code)
        with open(file_path, 'w') as file:
            file.write(code)
pattern = f'f"{year}/day_{{DAY:0>2}}_input"'
repl = f'f"{year}/input/day_{{DAY:0>2}}"'
for file_path in path.glob("day_[0-2][0-9].py"):
    with open(file_path, 'r') as file:
        code = file.read()
    if pattern in code:
        print(" ", file_path)
        code = code.replace(pattern, repl)
        with open(file_path, 'w') as file:
            file.write(code)
print("... finished")
