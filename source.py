from functions import *


def read_write_line():
    global line
    output_file.write(line)
    line = input_file.readline()


def read_x_y_m():
    global line
    x = y = m = None
    read_write_line()
    words = line.split()
    if words[0] == '[x]':
        x = words[1]
        read_write_line()
        words = line.split()
    if words[0] == '[y]':
        y = words[1]
        read_write_line()
        words = line.split()
    if words[0] == '[m]':
        m = words[1]
        output_file.write(line)
    return x, y, m


def return_answer(number):
    output_file.write('[answer] ' + str(number) + '\n')
    output_file.write('\n')


def return_answer_counters(number, countAdd, countMult):
    output_file.write('[answer] ' + str(number) + '\n')
    output_file.write('[count-add] ' + str(countAdd) + '\n')
    output_file.write('[count-mul] ' + str(countMult) + '\n')
    output_file.write('\n')


with open('output.txt', 'w') as output_file:
    with open('example.txt', 'r') as input_file:
        line = input_file.readline()
        while line:
            if line[0] == '#' or line[0] == ' ':
                pass
            else:
                words = line.split()
                if len(words) > 0:
                    if words[0] == '[radix]':
                        el_radix = int(words[1])
                        output_file.write(line)
                        el_m = None
                    if words[0] == '[add]':
                        el_x, el_y, el_m = read_x_y_m()
                        if el_m:
                            return_answer(modulo_add(el_x, el_y, el_m, el_radix))
                        else:
                            return_answer(add(el_x, el_y, el_radix))
                    if words[0] == '[subtract]':
                        el_x, el_y, el_m = read_x_y_m()
                        if el_m:
                            return_answer(modulo_subtract(el_x, el_y, el_m, el_radix))
                        else:
                            return_answer(subtract(el_x, el_y, el_radix))
                    if words[0] == '[multiply]':
                        el_x, el_y, el_m = read_x_y_m()
                        if el_m:
                            return_answer(modulo_multiply(el_x, el_y, el_m, el_radix))
                        else:
                            ans, count_add, count_mult = multiply(el_x, el_y, el_radix)
                            return_answer_counters(ans, count_add, count_mult)
                    if words[0] == '[inverse]':
                        el_x, el_y, el_m = read_x_y_m()
                        return_answer(modular_inversion(el_x, el_m, el_radix))
                    if words[0] == '[reduce]':
                        el_x, el_y, el_m = read_x_y_m()
                        return_answer(modular_reduction(el_x, el_m, el_radix))
                    if words[0] == '[euclid]':
                        el_x, el_y, el_m = read_x_y_m()
                        return_answer(euclid(el_x, el_y, el_radix))
                    if words[0] == '[karatsuba]':
                        el_x, el_y, el_m = read_x_y_m()
                        ans, count_add, count_mult = karatsuba(el_x, el_y, el_radix)
                        return_answer_counters(ans, count_add, count_mult)

            line = input_file.readline()

        print("\033[1;37;42m The script has succesfully finished, take a look in the output.txt file! \033[0m")
