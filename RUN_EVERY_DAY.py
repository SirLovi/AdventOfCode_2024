from bs4 import BeautifulSoup
import html2text
import requests
from os import path, makedirs

##################################################################################################

year_number = 2024

absolute_path = path.dirname(path.abspath(__file__))
session_id = ""
with open(absolute_path + "/SessionID.txt", "r") as file:
    session_id = file.read().rstrip()

##################################################################################################
# Iterate through all days (1 to 25)

for day_number in range(1, 26):
    print(f"Processing day {day_number}...")

    # Create directory for the day if it doesn't exist
    day_directory = f"./Day_{day_number:02d}"
    if not path.exists(day_directory):
        makedirs(day_directory)

    try:
        # Get and process the webpage
        raw_page_data = requests.get(
            f"https://adventofcode.com/{year_number}/day/{day_number}",
            headers={"cookie": f"session={session_id}"},
        ).text
        page_soup = BeautifulSoup(raw_page_data, "html.parser")
        articles = page_soup.findAll("article")

        # Get the input
        raw_input = requests.get(
            f"https://adventofcode.com/{year_number}/day/{day_number}/input",
            headers={"cookie": f"session={session_id}"},
        ).text.removesuffix("\n")

        # Save the input file
        with open(f"{day_directory}/input.txt", "w") as input_file:
            input_file.write(raw_input)

        # Write the webpage to Markdown
        h = html2text.HTML2Text()
        h.body_width = 0

        if len(articles) == 0:
            print(
                f"No articles were found for day {day_number}. This day has likely not been unlocked yet."
            )
            break

        with open(f"{day_directory}/instructions-one.md", "w") as article_one_file:
            article_one_file.write(h.handle(str(articles[0])).lstrip("\n").rstrip("\n"))

        if len(articles) > 1:
            with open(f"{day_directory}/instructions-two.md", "w") as article_two_file:
                article_two_file.write(
                    h.handle(str(articles[1])).lstrip("\n").rstrip("\n")
                )

        print(f"Day {day_number} processed successfully.")

    except Exception as e:
        print(f"An error occurred for day {day_number}: {e}")
