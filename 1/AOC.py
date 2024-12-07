##################################################################################################

from os import path

absolute_path = path.dirname(path.abspath(__file__))

##################################################################################################


def solve1():
    elf = [0]

    with open(absolute_path + "/input.txt", "r") as txtfile:
        i = 0

        lines = txtfile.readlines()

        for line in lines:

            if line.strip() == "":
                i = i + 1
                elf.append(0)
            else:
                elf[i] = elf[i] + int(line)

    print(max(elf))


##################################################################################################


def solve2():
    elf = [0]

    with open(absolute_path + "/input.txt", "r") as txtfile:
        i = 0

        lines = txtfile.readlines()

        for line in lines:

            if line.strip() == "":
                i = i + 1
                elf.append(0)
            else:
                elf[i] = elf[i] + int(line)
    elf.sort()

    three = elf[-1] + elf[-2] + elf[-3]

    print(three)


##################################################################################################


solve1()

solve2()

##################################################################################################
