
##################################################################################################

from os import path
import re
import string

absolute_path = path.dirname(path.abspath(__file__))

##################################################################################################


def solve1():

    sum = 0

    stacks = [[]]

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        
        lines = txtfile.readlines()

        stack_count = len(lines[0]) // 4
        

        stacks = [[] for _ in range(stack_count)]

        for line in lines:
            if line.strip().startswith("["):
                for i in range(stack_count):
                    letters = line[i*4:i*4+3]
                    if letters.startswith("["):
                        #print(line[1+4*i])
                        #print(letters)
                        stacks[i].insert(0,letters[1])

            elif line.strip().startswith("move"):
                parts = re.split(" ", line.strip())
                num_move = parts[1]
                place_from = parts[3]
                place_to = parts[5]

                #print(stack_count)

                for _ in range(int(num_move)):
                    stacks[int(place_to) - 1].append(stacks[int(place_from) - 1].pop())
                #print(num_move,place_from,place_to)
            

            #print(stacks)

    top_stacks = "".join([one[-1] for one in stacks])

    print(top_stacks,stacks)

##################################################################################################


def solve2():

    sum = 0

    stacks = [[]]

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        
        lines = txtfile.readlines()

        stack_count = len(lines[0]) // 4
        

        stacks = [[] for _ in range(stack_count)]

        for line in lines:
            if line.strip().startswith("["):
                for i in range(stack_count):
                    letters = line[i*4:i*4+3]
                    if letters.startswith("["):
                        #print(line[1+4*i])
                        #print(letters)
                        stacks[i].insert(0,letters[1])

            elif line.strip().startswith("move"):
                parts = re.split(" ", line.strip())
                num_move = parts[1]
                place_from = parts[3]
                place_to = parts[5]

                #print(stack_count)

                stacks[int(place_to)-1].extend(stacks[int(place_from)-1][-int(num_move):])

                del stacks[int(place_from)-1][-int(num_move):]
                #print(num_move,place_from,place_to)
            

            #print(stacks)

    top_stacks = "".join([one[-1] for one in stacks])

    print(top_stacks,stacks)

##################################################################################################


#solve1()

solve2()

##################################################################################################