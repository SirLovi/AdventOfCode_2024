import os
import requests
from bs4 import BeautifulSoup
import html2text
import time
import logging
import shutil

# This script fetches Advent of Code puzzle pages and inputs for a given year.
#
# Requirements:
#   - Ensure you have 'requests', 'beautifulsoup4', and 'html2text' installed:
#       pip install requests beautifulsoup4 html2text
#
# Usage:
#   python RUN_EVERY_DAY.py
#
# The script will:
#   - Attempt to read the Advent of Code session ID from a file named "SessionID.txt" in the current directory.
#   - If not found, prompt the user for the session ID.
#   - Fetch puzzle pages and inputs for the specified year from Advent of Code.
#   - Create directories "Day_01" through "Day_25" as puzzles become available.
#   - Write `input_XX.txt`, `instructions-one.md`, and `instructions-two.md` (if the second part is available)
#     into each day's directory.
#   - Copy `AOC_TEMPLATE.py` into each day's directory as `Solution_XX.py`.
#   - Stop fetching when it encounters a day that's not yet available.
#
# Notes:
#   - The script uses logging to record progress and errors in 'aoc_fetch.log' and sleeps 1 second between requests.
#   - Add `SessionID.txt` to `.gitignore` to avoid committing your session key.

##################################################################################################
# Configuration
##################################################################################################

year_number = 2024
template_file = (
    "AOC_TEMPLATE.py"  # The template that will be copied into each day's folder
)

logging.basicConfig(
    filename="aoc_fetch.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

##################################################################################################
# Session ID Handling
##################################################################################################

# 1. Check environment variable
session_id = os.environ.get("AOC_SESSION_ID")

# 2. If not found in environment, try reading from file
if not session_id:
    session_id_file = "SessionID.txt"
    if os.path.exists(session_id_file):
        with open(session_id_file, "r") as f:
            session_id = f.read().strip()

# 3. If still not found, prompt the user
if not session_id:
    session_id = input(
        "No session ID found. Please enter your Advent of Code session ID: "
    ).strip()

# Ensure the environment variable is set (for consistency)
os.environ["AOC_SESSION_ID"] = session_id

print("Starting to fetch Advent of Code data...")

##################################################################################################
# Helper Function
##################################################################################################


def get_example(day, offset=0, year=year_number):
    """
    Retrieves the example input(s) from the AoC puzzle page.
    The offset parameter can be used if multiple examples exist.
    """
    AOC_SessionID = session_id  # Use the globally defined session_id
    url = f"https://adventofcode.com/{year}/day/{day}"
    logging.info(f"Fetching puzzle page from {url} for example extraction")
    response = requests.get(url, headers={"cookie": f"session={AOC_SessionID}"})
    if response.status_code != 200:
        logging.warning(
            f"Unable to fetch puzzle page for examples (HTTP {response.status_code})."
        )
        return ""

    # Parse out the examples. This is a simplistic approach and may need adjustments if AoC changes format.
    parts = response.text.split("<pre><code>")
    if len(parts) > offset + 1:
        example_part = parts[offset + 1].split("</code></pre>")[0].strip()
        return example_part
    else:
        logging.info("No example found at the given offset.")
        return ""


##################################################################################################
# Main logic
##################################################################################################

for day_number in range(1, 26):
    print(f"Processing day {day_number}...")
    logging.info(f"Processing day {day_number}...")

    day_directory = f"./Day_{day_number:02d}"
    os.makedirs(day_directory, exist_ok=True)

    puzzle_url = f"https://adventofcode.com/{year_number}/day/{day_number}"

    try:
        # Fetch puzzle page
        puzzle_response = requests.get(
            puzzle_url, headers={"cookie": f"session={session_id}"}
        )

        # Check if puzzle is not available
        if puzzle_response.status_code == 404:
            logging.warning(f"Day {day_number}: Puzzle not available (404). Stopping.")
            print(f"Day {day_number} puzzle not yet available. Stopping.")
            break
        elif puzzle_response.status_code != 200:
            logging.warning(
                f"Day {day_number}: Received status code {puzzle_response.status_code}, skipping this day."
            )
            print(
                f"Warning: Received status code {puzzle_response.status_code} for day {day_number}. Skipping."
            )
            continue

        page_soup = BeautifulSoup(puzzle_response.text, "html.parser")
        articles = page_soup.findAll("article")

        if not articles:
            logging.info(
                f"No articles found for day {day_number}, puzzle not released yet."
            )
            print(f"No puzzle content for day {day_number}, stopping.")
            break

        # Fetch puzzle input
        input_url = f"https://adventofcode.com/{year_number}/day/{day_number}/input"
        input_response = requests.get(
            input_url, headers={"cookie": f"session={session_id}"}
        )

        if input_response.status_code == 200:
            raw_input = input_response.text.rstrip("\n")
            input_filename = f"input_{day_number:02d}.txt"  # Changed here
            with open(f"{day_directory}/{input_filename}", "w") as input_file:
                input_file.write(raw_input)
            print(
                f"Input for day {day_number} fetched successfully as {input_filename}."
            )
        else:
            logging.warning(
                f"Day {day_number}: Input not available (status {input_response.status_code})."
            )
            print(
                f"Warning: Input not available for day {day_number}. (status {input_response.status_code})"
            )

        # Convert articles to markdown
        h = html2text.HTML2Text()
        h.body_width = 0

        # instructions-one.md
        instructions_one_path = f"{day_directory}/instructions-one.md"
        with open(instructions_one_path, "w") as article_one_file:
            article_one_file.write(h.handle(str(articles[0])).strip("\n"))
        print(f"Saved instructions-one.md for day {day_number}.")

        # instructions-two.md (if exists)
        if len(articles) > 1:
            instructions_two_path = f"{day_directory}/instructions-two.md"
            with open(instructions_two_path, "w") as article_two_file:
                article_two_file.write(h.handle(str(articles[1])).strip("\n"))
            print(f"Saved instructions-two.md for day {day_number}.")

        # Fetch the first example and save it if exists
        example = get_example(day=day_number, offset=0, year=year_number)
        if example:
            example_path = f"{day_directory}/Example_{day_number:02d}.txt"
            with open(example_path, "w") as example_file:
                example_file.write(example)
            print(f"Saved Example_{day_number:02d}.txt for day {day_number}.")
        else:
            print(f"No example found for day {day_number}.")

        # Copy AOC_TEMPLATE.py into the day's directory as Solution_XX.py
        solution_filename = f"Solution_{day_number:02d}.py"
        solution_path = os.path.join(day_directory, solution_filename)
        if os.path.exists(template_file):
            shutil.copyfile(template_file, solution_path)
            print(f"Copied {template_file} to {solution_path}")
        else:
            logging.warning(
                f"{template_file} not found. Skipping template copy for day {day_number}."
            )
            print(
                f"Warning: {template_file} not found. Template not copied for day {day_number}."
            )

        logging.info(f"Day {day_number} processed successfully.")
        print(f"Day {day_number} processed successfully.")

        # Wait a bit before processing the next day
        time.sleep(1)

    except Exception as e:
        logging.error(f"An error occurred for day {day_number}: {e}")
        print(f"Error for day {day_number}: {e}")

print("Done fetching Advent of Code data.")
