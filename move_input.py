import re
import sys
from argparse import ArgumentParser
from pathlib import Path


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
for file_path in path.glob("day_[0-2][0-9]_input*.*"):
    print(file_path)
