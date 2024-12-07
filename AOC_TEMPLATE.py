'''
Advent of Code automation template - @MathisHammel

This template provides functions to download inputs and submit answers on AoC.

You need to paste your adventofcode.com session cookie below.
If you don't know how to get this cookie, here's a quick tutorial:
- Open your browser and go to adventofcode.com, make sure you are logged in
- Open the developer console (Ctrl+Shift+I on Firefox/Chrome)
- Get the value of your session cookie:
      - Chrome : 'Application' tab > Cookies
      - Firefox : 'Storage' tab > Cookies
- The cookie is a string of 96 hexadecimal characters, paste it in the AOC_SessionID below.

Your cookie is similar to a password, >>> DO NOT SHARE/PUBLISH IT <<<
If you intend to share your solutions, store it in an env variable or a file.
'''
##################################################################################################

import requests
from os import path

##################################################################################################

absolute_path = path.dirname(path.abspath(__file__))
AOC_SessionID = ''
YEAR = '2022'

with open(absolute_path + '/SessionID.txt', 'r') as file:
    AOC_SessionID = file.read().rstrip()

##################################################################################################


def get_input(day):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}/input',
                       headers={'cookie': 'session='+AOC_SessionID})
    return req.text


def get_example(day, offset=0):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}',
                       headers={'cookie': 'session='+AOC_SessionID})
    return req.text.split('<pre><code>')[offset+1].split('</code></pre>')[0]


def submit(day, level, answer):
    print(f'You are about to submit the follwing answer:')
    print(f'>>>>>>>>>>>>>>>>> {answer}')
    input('Press enter to continue or Ctrl+C to abort.')
    data = {
        'level': str(level),
        'answer': str(answer)
    }

    response = requests.post(f'https://adventofcode.com/{YEAR}/day/{day}/answer',
                             headers={'cookie': 'session='+AOC_SessionID}, data=data)
    if 'You gave an answer too recently' in response.text:
        # You will get this if you submitted a wrong answer less than 60s ago.
        print('VERDICT : TOO MANY REQUESTS')
    elif 'not the right answer' in response.text:
        if 'too low' in response.text:
            print('VERDICT : WRONG (TOO LOW)')
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
        else:
            print('VERDICT : WRONG (UNKNOWN)')
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')

##################################################################################################


DAY = 1
PART = 1

s = get_input(DAY).strip()  # the daily input is stored in s
ex = get_example(DAY).strip()  # the daily example is stored in ex

##################################################################################################


def solve1(data):
    currpos = 0
    currdepth = 0

    for i in range(0, len(data)):
        if(data[i] == "forward"):
            currpos += int(data[i+1])
        elif(data[i] == "down"):
            currdepth += int(data[i+1])
        elif(data[i] == "up"):
            currdepth -= int(data[i+1])

    print("\n1:")
    print("Final Position: ", currpos)
    print("Final Depth: ", currdepth)
    print("Multiplied: ", currdepth*currpos)

##################################################################################################


def solve2(data):
    currpos = 0
    currdepth = 0
    aim = 0

    for i in range(0, len(data)):
        if(data[i] == "forward"):
            currpos += int(data[i+1])
            currdepth += aim * int(data[i+1])
        elif(data[i] == "down"):
            aim += int(data[i+1])
        elif(data[i] == "up"):
            aim -= int(data[i+1])

    print("\n1:")
    print("Final Position: ", currpos)
    print("Final Depth: ", currdepth)
    print("Multiplied: ", currdepth*currpos)

##################################################################################################


with open(absolute_path + "/input.txt", 'r') as txtfile:
    data = [str(val) for curr_line in txtfile.readlines()
            for val in curr_line.split()]

# print(data)

# solve1(data)

# solve2(data)

##################################################################################################

ans = 123

submit(DAY, PART, ans)
