"""
Advent of Code Automation Template
----------------------------------
This script provides functions to:
- Retrieve the session ID from environment variables or a local file (SessionID.txt).
- Fetch puzzle input for a given year/day.
- Dynamically determine DAY and PART based on directory and available instructions.
- Submit solutions (with a prompt or automatic if configured).
"""

import os
import sys
import time
import logging
import requests
from pathlib import Path
import re

##################################################################################################
# Configuration
##################################################################################################

BASE_DIR = Path(__file__).parent.resolve()

# Extract DAY from directory name, assuming directory is named like "Day_04"
# This pattern finds integers in the directory name.
day_match = re.search(r"(\d+)", BASE_DIR.name)
if day_match:
    DAY = int(day_match.group(1))
else:
    print(
        "Could not determine the day from the directory name. Please rename directory to something like Day_01."
    )
    sys.exit(1)

# Determine PART based on whether instructions-two.md exists
instructions_two_file = BASE_DIR / "instructions-two.md"
if instructions_two_file.exists():
    PART = 2
else:
    PART = 1

YEAR = "2024"  # Update this each year as needed

INPUT_FILE = BASE_DIR / "input.txt"
SESSION_FILE = BASE_DIR / "SessionID.txt"

# Setup logging
LOG_FILE = BASE_DIR / "aoc_solution.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

##################################################################################################
# Session Handling
##################################################################################################

AOC_SessionID = os.environ.get("AOC_SESSION_ID")

if not AOC_SessionID and SESSION_FILE.exists():
    with open(SESSION_FILE, "r") as f:
        AOC_SessionID = f.read().strip()

if not AOC_SessionID:
    AOC_SessionID = input(
        "No session ID found. Please enter your AoC session ID: "
    ).strip()

if not AOC_SessionID:
    logging.error("Invalid or missing session ID. Exiting.")
    print("Error: A valid Advent of Code session cookie must be provided.")
    sys.exit(1)

os.environ["AOC_SESSION_ID"] = AOC_SessionID

##################################################################################################
# Functions
##################################################################################################


def get_input(day, year=YEAR):
    """
    Retrieves the input for the specified AoC day and year.
    If available locally, uses the cached version. Otherwise, fetches from AoC.
    """
    if INPUT_FILE.exists():
        logging.info(f"Using cached input for day {day}, year {year}.")
        with open(INPUT_FILE, "r") as f:
            return f.read()

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    logging.info(f"Fetching input from {url}")
    response = requests.get(url, headers={"cookie": f"session={AOC_SessionID}"})

    if response.status_code == 200:
        data = response.text
        with open(INPUT_FILE, "w") as f:
            f.write(data)
        return data
    else:
        logging.error(f"Failed to fetch input: HTTP {response.status_code}")
        print(
            f"Error: Unable to fetch input (status code {response.status_code}). Check session ID."
        )
        sys.exit(1)


def submit(day, level, answer, year=YEAR, auto_submit=False):
    """
    Submits the specified answer for the given AoC puzzle day and level.
    Logs the submission and result.

    If auto_submit is False, prompts the user before submitting.
    If auto_submit is True, submits without prompting.

    NOTE: Consider using this function with caution to avoid accidental submissions.
    """
    print(
        f"\nPreparing to submit answer for Year {year}, Day {day}, Level {level}: {answer}"
    )
    if not auto_submit:
        user_input = input("Press Enter to submit or Ctrl+C to abort... ")

    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {"level": str(level), "answer": str(answer)}

    logging.info(f"Submitting answer for day {day}, level {level}.")
    response = requests.post(
        url, headers={"cookie": f"session={AOC_SessionID}"}, data=data
    )
    text = response.text

    if "You gave an answer too recently" in text:
        verdict = "TOO MANY REQUESTS"
    elif "not the right answer" in text:
        if "too low" in text:
            verdict = "WRONG (TOO LOW)"
        elif "too high" in text:
            verdict = "WRONG (TOO HIGH)"
        else:
            verdict = "WRONG (UNKNOWN)"
    elif "seem to be solving the right level." in text:
        verdict = "ALREADY SOLVED"
    else:
        verdict = "OK!"

    logging.info(f"Submission result for day {day}, level {level}: {verdict}")
    print(f"VERDICT: {verdict}")


##################################################################################################
# Example Solution Functions (Replace with your day's logic)
##################################################################################################


def solve_part1(puzzle_input):

    # Implement logic for part 1 here
    lines = puzzle_input.strip().split("\n")
    # Example logic: just count lines
    result = len(lines)

    return result


def solve_part2(puzzle_input):

    # Implement logic for part 2 here
    lines = puzzle_input.strip().split("\n")
    # Example logic: sum length of lines
    result = sum(len(line) for line in lines)

    return result


##################################################################################################
# Main Execution Logic
##################################################################################################

if __name__ == "__main__":
    logging.info(f"Starting AoC Template Script for Day {DAY}, PART {PART}")
    puzzle_input = get_input(DAY).strip()

    # Choose the solver based on PART
    if PART == 1:
        answer = solve_part1(puzzle_input)
    else:
        answer = solve_part2(puzzle_input)

    # Change auto_submit to True to skip the prompt
    submit(DAY, PART, answer, auto_submit=False)

    print("Done.")
