from AddMultSubt import add, subtract, multiply, hexToNumber, numberToHex, modular_reduction, modular_inversion, \
    division_without_rest


def hexToDecimal(number):
    n = 0
    for i in range(len(number)):
        n = n + 16 ** (len(number) - 1 - i) * int(hexToNumber(number[i]))
    return n


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
        output_file.write(line)
    return x, y, m


def return_answer(number):
    output_file.write('[answer] ' + str(number) + '\n')


def return_answer_counters(number, countAdd, countMult):
    output_file.write('[answer] ' + str(number) + '\n')
    output_file.write('[count-add] ' + str(countAdd) + '\n')
    output_file.write('[count-mul] ' + str(countMult) + '\n')


def modulo_add(x, y, m, radix):
    ans = add(x, y, radix)
    ans = hexToDecimal(ans)
    m = hexToDecimal(m)
    while (ans >= m):
        ans = ans - m
    ans = hex(ans).split('x')[-1]
    return str(ans)


def modulo_subtract(x, y, m, radix):
    ans = subtract(x, y, radix)
    if (ans[0] == '-'):
        ans = hexToDecimal(ans[1:])
        ans *= -1
        m = hexToDecimal(m)
        while (ans < 0):
            ans = ans + m
    else:
        ans = hexToDecimal(ans)
    ans = hex(ans).split('x')[-1]
    return str(ans)


def modulo_multiply(x, y, m, radix):
    ans = multiply(x, y, radix)[0]
    ans = modular_reduction(ans, m, radix)
    return str(ans)


def inverse(x, m, radix):
    pass


def reduce(x, m, radix):
    pass


def euclid(x, y, radix):
    pass


def karatsuba(el_x, el_y, el_radix):
    pass


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
                        # print(line, end='')
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
                            ans, count1, count2 = multiply(el_x, el_y, el_radix)
                            return_answer_counters(ans, count1, count2)
                    if words[0] == '[inverse]':
                        el_x, el_y, el_m = read_x_y_m()
                        return_answer(inverse(el_x, el_m, el_radix))
                    if words[0] == '[reduce]':
                        el_x, el_y, el_m = read_x_y_m()
                        return_answer(reduce(el_x, el_m, el_radix))
                    if words[0] == '[euclid]':
                        el_x, el_y, el_m = read_x_y_m()
                        euclid(el_x, el_y, el_radix)
                    if words[0] == '[karatsuba]':
                        el_x, el_y, el_m = read_x_y_m()
                        karatsuba(el_x, el_y, el_radix)

            line = input_file.readline()
