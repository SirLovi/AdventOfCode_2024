
##################################################################################################

from os import path
import string

absolute_path = path.dirname(path.abspath(__file__))

##################################################################################################

def splitword(w):
    split = -((-len(w))//2)
    return w[:split], w[split:]


def solve1():

    priorities = {letter: str(index) for index, letter in enumerate(string.ascii_letters, start=1)} 
    sum = 0

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        lines = txtfile.readlines()
        

        for line in lines:
            half1, half2 = splitword(line.strip())
            common = ''.join(set(half1).intersection(half2))
            #print(half1,half2,common)
            sum = sum + int(priorities[common])

    print(sum)

##################################################################################################

def solve2():

    priorities = {letter: str(index) for index, letter in enumerate(string.ascii_letters, start=1)} 
    sum = 0

    with open(absolute_path + "/input.txt", 'r') as txtfile:
        lines = txtfile.readlines()
        
        counter = 0
        elf1 = set()
        elf2 = set()
        elf3 = set()
        for line in lines:

            match counter:
                case 0:
                    elf1 = set(line.strip())
                case 1:
                    elf2 = set(line.strip())
                case 2:
                    elf3 = set(line.strip())

                    elf12 = elf1.intersection(elf2)
                    common = ''.join(set(elf12).intersection(elf3))
                    #print(elf1,elf2,elf3,common)
                    sum = sum + int(priorities[common])

            counter = counter + 1
            if counter >= 3: counter = 0

    print(sum)

##################################################################################################


#solve1()

solve2()

##################################################################################################