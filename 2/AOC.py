
##################################################################################################

from os import path

absolute_path = path.dirname(path.abspath(__file__))

##################################################################################################
POINTS_X = 1
POINTS_Y = 2
POINTS_Z = 3
POINTS_LOST = 0
POINTS_DRAW = 3
POINTS_WIN = 6

def solve1():

    score = 0

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        
        lines = txtfile.readlines()

        for line in lines:
            line.strip()
            
            if (line[0] == "A") & (line[2] == "X"):
                score = score + POINTS_X + POINTS_DRAW
            elif (line[0] == "A") & (line[2] == "Y"):
                score = score + POINTS_Y + POINTS_WIN
            elif (line[0] == "A") & (line[2] == "Z"):
                score = score + POINTS_Z + POINTS_LOST
            elif (line[0] == "B") & (line[2] == "X"):
                score = score + POINTS_X + POINTS_LOST
            elif (line[0] == "B") & (line[2] == "Y"):
                score = score + POINTS_Y + POINTS_DRAW
            elif (line[0] == "B") & (line[2] == "Z"):
                score = score + POINTS_Z + POINTS_WIN
            elif (line[0] == "C") & (line[2] == "X"):
                score = score + POINTS_X + POINTS_WIN
            elif (line[0] == "C") & (line[2] == "Y"):
                score = score + POINTS_Y + POINTS_LOST
            elif (line[0] == "C") & (line[2] == "Z"):
                score = score + POINTS_Z + POINTS_DRAW
            
            
            else:
                print("Else")

    print(score)

##################################################################################################


def solve2():
    score = 0

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        
        lines = txtfile.readlines()

        for line in lines:
            line.strip()
            # ROCK
            # PAPER
            # SCISSORS
            if (line[0] == "A") & (line[2] == "X"):
                score = score + POINTS_Z + POINTS_LOST
            elif (line[0] == "A") & (line[2] == "Y"):
                score = score + POINTS_X + POINTS_DRAW
            elif (line[0] == "A") & (line[2] == "Z"):
                score = score + POINTS_Y + POINTS_WIN
            elif (line[0] == "B") & (line[2] == "X"):
                score = score + POINTS_X + POINTS_LOST
            elif (line[0] == "B") & (line[2] == "Y"):
                score = score + POINTS_Y + POINTS_DRAW
            elif (line[0] == "B") & (line[2] == "Z"):
                score = score + POINTS_Z + POINTS_WIN
            elif (line[0] == "C") & (line[2] == "X"):
                score = score + POINTS_Y + POINTS_LOST
            elif (line[0] == "C") & (line[2] == "Y"):
                score = score + POINTS_Z + POINTS_DRAW
            elif (line[0] == "C") & (line[2] == "Z"):
                score = score + POINTS_X + POINTS_WIN
            
            
            else:
                print("Else")

    print(score)

##################################################################################################


#solve1()

solve2()

##################################################################################################