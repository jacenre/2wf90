from AddMultSubt import add, subtract, multiply

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
    output_file.write('[answer] ' + number +'\n')


def modulo_add(x, y, m, radix):
    pass


def modulo_subtract(x, y, m, radix):
    pass


def modulo_multiply(x, y, m, radix):
    pass


def inverse(x, m, radix):
    pass


def reduce(x, m, radix):
    pass


def euclid(x, y, radix):
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
                        print(line, end='')
                        el_m = None
                    if words[0] == '[add]':
                        el_x, el_y, el_m = read_x_y_m()
                        if el_m:
                            modulo_add(el_x, el_y, el_m, el_radix)
                        else:
                            add(el_x, el_y, el_radix)
                    if words[0] == '[subtract]':
                        el_x, el_y, el_m = read_x_y_m()
                        if el_m:
                            modulo_subtract(el_x, el_y, el_m, el_radix)
                        else:
                            subtract(el_x, el_y, el_radix)
                    if words[0] == '[multiply]':
                        el_x, el_y, el_m = read_x_y_m()
                        if el_m:
                            modulo_multiply(el_x, el_y, el_m, el_radix)
                        else:
                            multiply(el_x, el_y, el_radix)
                    if words[0] == '[inverse]':
                        el_x, el_y, el_m = read_x_y_m()
                        inverse(el_x,el_m,el_radix)
                    if words[0] == '[reduce]':
                        el_x, el_y, el_m = read_x_y_m()
                        reduce(el_x,el_m,el_radix)
                    if words[0] =='[euclid]':
                        el_x, el_y, el_m = read_x_y_m()
                        euclid(el_x,el_y,el_radix)
            line = input_file.readline()
