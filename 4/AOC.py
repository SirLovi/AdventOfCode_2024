
##################################################################################################

from os import path
import re

absolute_path = path.dirname(path.abspath(__file__))

##################################################################################################


def solve1():

    sum = 0

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        
        lines = txtfile.readlines()

        for line in lines:
            
            parts = re.split("-|,", line.strip())
            #print(parts)
            group1 = set(range(int(parts[0]),int(parts[1])+1))
            group2 = set(range(int(parts[2]),int(parts[3])+1))
            
            if group1.issubset(group2): sum = sum+1
            elif group2.issubset(group1): sum = sum+1

    print(sum)

##################################################################################################


def solve2():

    sum = 0

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        
        lines = txtfile.readlines()

        for line in lines:
            
            parts = re.split("-|,", line.strip())
            #print(parts)
            group1 = set(range(int(parts[0]),int(parts[1])+1))
            group2 = set(range(int(parts[2]),int(parts[3])+1))
            
            if len(group1.intersection(group2)) > 0: sum = sum+1

    print(sum)

##################################################################################################


#solve1()

solve2()

##################################################################################################