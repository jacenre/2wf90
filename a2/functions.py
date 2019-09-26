import math, re


def parseInput(input):
  data = {}
  for i in range(len(input)):
    line = re.sub('/[\n\r]/g', '', input[i])
    argument, n = line.split('[')[1].split(']')
    data[argument] = n.strip()
  return data

def parseOutput(obj):
    output = ''
    for argument in obj:
        output += '[%s] %s\n' % (argument, obj[argument])
    return output

def getMethod(computation):
  for argument in computation:
    if computation[argument] == '':
      del computation[argument]
      return argument
  return None

#convert hex symbol to number
def hexToNumber(x):
    if x == "a":
        x = "10"
    elif x == "b":
        x = "11"
    elif x == "c":
        x = "12"
    elif x == "d":
        x = "13"
    elif x == "e":
        x = "14"
    elif x == "f":
        x = "15"
    return x
#convert number to hex symbol


def numberToHex(x):
    if x == "10":
        x = "a"
    elif x == "11":
        x = "b"
    elif x == "12":
        x = "c"
    elif x == "13":
        x = "d"
    elif x == "14":
        x = "e"
    elif x == "15":
        x = "f"
    return x  
    
# function for addition
def add(x, y, radix):
    answer = ''
    carry = 0

    #check if numbers are negative
    negative = False
    if x[0] == '-':
        if y[0] == '-':             # -x + -y = -(x + y)
            x = x[1:]               # remove minus sign
            y = y[1:]               # remove minus sign
            negative = True
        else:
            return subtract(y, x[1:], radix)        # -x + y = y - x
    if y[0] == '-':
        return subtract(x, y[1:], radix)            # x + -y = x - y

    # add leading 0's to number with smallest length
    maxlength = max(len(x), len(y))
    if maxlength == len(x):
        y = (len(x) - len(y)) * "0" + y
    elif maxlength == len(y):
        x = (len(y) - len(x)) * "0" + x

    for i in range(len(x)-1, -1, -1):
        x_i = hexToNumber(x[i])
        y_i = hexToNumber(y[i])
        z_i = int(x_i) + int(y_i) + carry           # z_i = x_i + y_i + c
        carry = math.floor(z_i/radix)
        z_i = z_i % radix
        answer = numberToHex(str(z_i)) + answer

    if carry > 0:
        answer = numberToHex(str(carry)) + answer

    if negative:
        # if negative is true, add minus sign to answer
        answer = "-" + answer

    return answer

#function for subtraction


def subtract(x, y, radix):
    if x == y:
        return "0"

    answer = ''
    carry = 0

    #check if numbers are negative
    if x[0] == '-':
        if y[0] == '-':                             # -x - -y = -x + y = y - x
            return subtract(y[1:], x[1:], radix)
        else:
            answer = "-" + add(x[1:], y, radix)     # -x - y = - (x + y)
            return answer
    if y[0] == '-':
        return add(x, y[1:], radix)                 # x - -y = x + y

    # add leading 0's to number with smallest length
    if max(len(x), len(y)) == len(x):
        y = (len(x) - len(y)) * "0" + y
    elif max(len(x), len(y)) == len(y):
        x = (len(y) - len(x)) * "0" + x

    for i in range(len(x)-1, -1, -1):
        x_i = hexToNumber(x[i])
        y_i = hexToNumber(y[i])
        z_i = int(x_i) - int(y_i) + carry
        carry = math.floor(z_i/radix)
        z_i = ((z_i % radix) + radix) % radix
        answer = numberToHex(str(z_i)) + answer

    # if number becomes negative after subtraction
    if carry < 0:
        answer = list(answer)
        answer[len(answer)-1] = int(hexToNumber(answer[len(answer)-1])) - 1
        for i in range(0, len(answer)):
            answer[i] = numberToHex(
                str((radix - 1) - int(hexToNumber(answer[i]))))
        answer = ''.join(answer)
        answer = answer.lstrip("0")  # remove leading 0's
        answer = '-' + answer

    # remove leading 0's
    answer = answer.lstrip("0")

    return answer

#function for multiplication


def multiply(x, y, radix):
    # count total number of elementary additions/subtractions
    countAdd = 0
    # count total number of elementary multiplications
    countMult = 0

    if x == "0" or y == "0":
        return ("0", countAdd, countMult)

    answer = ["0"] * (len(x) + len(y))

    #check if numbers are negative
    negative = False
    if x[0] == '-':
        negative = not negative
        x = x[1:]                           # remove minus sign
    if y[0] == '-':
        negative = not negative
        y = y[1:]                           # remove minus sign

    # Reverse the strings, so the i and j are the same as in the algorithm 1.3 decription
    x = list(x)
    x.reverse()
    x = ''.join(x)
    y = list(y)
    y.reverse()
    y = ''.join(y)

    for i in range(0, len(x)):
        countAdd = countAdd + 1
        c = 0
        for j in range(0, len(y)):
            countAdd = countAdd + 1
            first = hexToNumber(x[i])
            second = hexToNumber(y[j])

            t = int(hexToNumber(answer[i + j])) + int(first) * int(second) + c
            countAdd = countAdd + 3
            countMult = countMult + 1

            c = math.floor(t / radix)
            countMult = countMult + 1

            answer[i+j] = numberToHex(str(t - c * radix))
            countAdd = countAdd + 2
            countMult = countMult + 1

        answer[i + len(y)] = str(numberToHex(c))
        countAdd = countAdd + 1
        for u in range(0, len(answer)):
            answer[u] = numberToHex(answer[u])

    k = len(x) + len(y)
    countAdd = countAdd + 1

    if answer[len(x) + len(y) - 1] == "0":
        k = k - 1
        countAdd = countAdd + 1
    countAdd = countAdd + 1

    # reverse answer
    answer = answer[0:k]
    answer.reverse()
    answer = ''.join(answer)

    if negative:
        answer = '-' + answer               # if negative, add minus sign

    return (answer, countAdd, countMult)

# function for modular reduction, algorithm 2.5


def modular_reduction(x, m, radix):
    # check if x is negative
    negative = False
    if x[0] == "-":
        negative = True
        x_prime = x[1:]             # remove minus sign
    else:
        x_prime = x

    # k = word size of x, n = word size of m
    k = len(x_prime)
    n = len(m)

    for i in range(k - n, -1, -1):
        # m * b^i is equal to left-shifting m by i positions, so we add i*0 to the right side of the string
        m_left_shift = m + i * "0"

        # We need to know if x is larger than m * b^i, so we subtract m * b^i from x to see if the result is negative
        x_subtract_left_shifted_m = subtract(x_prime, m_left_shift, radix)

        # While the result of x - m * b^i is not negative
        while x_subtract_left_shifted_m[0] != "-":
            # x' = x - m * b^i
            x_prime = x_subtract_left_shifted_m
            x_subtract_left_shifted_m = subtract(
                x_prime, m_left_shift, radix)      # update for new x'

    if (negative == False) or (x_prime == '0'):             # if x > 0 or x' = 0
        result = x_prime                                    # return x'
    else:
        # else return m - x'
        result = subtract(m, x_prime, radix)
    return result

# function for modular inversion, algorithm 2.11


def modular_inversion(x, m, radix):
    a_prime = x
    m_prime = m
    x_1 = '1'
    x_2 = '0'

    while m_prime != "0" and m_prime[0] != "-":                 # while m' > 0
        # q = math.floor(a_prime / m_prime)
        q = division_without_rest(a_prime, m_prime, radix)

        q_mult_m_prime = multiply(q, m_prime, radix)            # q * m'
        # multiply() returns an array, take only first element
        q_mult_m_prime = q_mult_m_prime[0]

        # r = a' - q * m'
        r = subtract(a_prime, q_mult_m_prime, radix)

        a_prime = m_prime                                       # a' = m'
        m_prime = r                                             # m' = r

        q_mult_x_2 = multiply(q, x_2, radix)                    # q * x_2
        # multiply() returns an array, take only first element
        q_mult_x_2 = q_mult_x_2[0]

        # x_3 = x_1 - q * x_2
        x_3 = subtract(x_1, q_mult_x_2, radix)
        x_1 = x_2                                               # x_1 = x_2
        x_2 = x_3                                               # x_2 = x_3
    if a_prime == "1":
        # apparently there exists both a negative and a positive inverse modulo,
        # function may return negative modulo
        # change negative to positive modulo
        if x_1[0] == "-":
            # m - x_1 returns positive inverse modulo
            x_1 = subtract(m, x_1[1:], radix)
        return x_1
    else:
        # if no inverse exists, error
        return "inverse does not exist"

# returns z with x = zy == math.floor of dividing two numbers
# needed for modular_inversion() and euclid()


def division_without_rest(x, y, radix):
    c = 0                                                       # set count to 0
    # answer is empty string
    answer = ""
    subtract_x_y = subtract(x, y, radix)                        # x - y

    #subtract y from x, every subtraction => increment c
    while subtract_x_y[0] != "-":                               # while x > y
        x = subtract_x_y                                        # x = x - y
        c = c + 1                                               # increment count
        subtract_x_y = subtract(x, y, radix)                    # x - y

    #change c to correct base
    if c >= radix:
        while math.floor(c / radix) > 0:
            answer = numberToHex(str(c % radix)) + answer
            c = math.floor(c / radix)

        # do operation once more after loop has ended
        c = numberToHex(str(c % radix)) + answer
    else:
        c = numberToHex(str(c))
    return c

# function for modular addition, algorithm 2.7


def modulo_add(x, y, m, radix):
    z_prime = add(x, y, radix)                      # z' = x + y
    # if z' < m then m - z' is not negative
    if subtract(m, z_prime, radix)[0] != "-":
        z = z_prime                                 # z = z'
    else:
        z = subtract(z_prime, m, radix)             # z = z' - m
    return z

# function for modular subtraction, algorithm 2.8


def modulo_subtract(x, y, m, radix):
    z_prime = subtract(x, y, radix)                 # z' = x + y
    if z_prime[0] != "-":                           # if z' >= 0, i.e. z' is not negative
        z = z_prime                                 # z = z'
    else:
        z = add(z_prime, m, radix)             # z = z' + m
    return z

# function for modular multiplication, algorithm 2.9 (naive)


def modulo_multiply(x, y, m, radix):
    ans = multiply(x, y, radix)[0]          # z' = x * y
    ans = modular_reduction(ans, m, radix)    # z = z' (mod m)
    return ans

# returns absolute value of x by removing the minus sign if present
# used by euclid()


def abs_value(x):
    if x[0] == '-':
        x = x[1:]
    return x

# function for extended euclidean algorithm, algorithm 2.2


def euclid(x, y, radix):
    a = x
    b = y
    x = abs_value(x)
    y = abs_value(y)
    x1 = '1'
    x2 = '0'
    y1 = '0'
    y2 = '1'
    radix = int(radix)
    while y[0] != '-' and y[0] != '0':
        q = division_without_rest(x, y, radix)
        r = subtract(x, multiply(q, y, radix)[0], radix)
        x = y
        y = r
        x3 = subtract(x1, multiply(q, x2, radix)[0], radix)
        y3 = subtract(y1, multiply(q, y2, radix)[0], radix)
        x1 = x2
        y1 = y2
        x2 = x3
        y2 = y3
    if a[0] != '-':
        ret1 = x1
    else:
        ret1 = '-' + x1
    if b[0] != '-':
        ret2 = y1
    else:
        ret2 = '-' + y1

    return x, ret1, ret2

# function for removing leading zero's, unless value is 0
# used by karatsuba()


def remove_leading_zeros(a):
    # if there's a leading 0 remove it unless it's the only 0
    while a[0] == '0' and len(a) > 1:
        a = a[1:]
    return a

# function for Karatsuba multiplication
# countAdd and countMult are necessary as arguments, because Karatsuba works recursively


def karatsuba(x, y, radix, countAdd, countMult):
    negative = False
    if x[0] == '-':
        negative = not negative
        x = x[1:]
    if y[0] == '-':
        negative = not negative
        y = y[1:]
    result = ''
    if negative:
        result = '-'
    answer = compute_karatsuba(x, y, radix, countAdd, countMult)
    # (result, countAdd, countMult)
    return result + answer[0], answer[1], answer[2]

# function for Karatsuba


def compute_karatsuba(x, y, radix, countAdd, countMult):

    # add leading 0's to number with smallest length
    if max(len(x), len(y)) == len(x):
        y = (len(x) - len(y)) * "0" + y
    elif max(len(x), len(y)) == len(y):
        x = (len(y) - len(x)) * "0" + x

    n = len(x)

    if n == 1:  # if there's just one digit, simply do the normal multiply
        answer = multiply(x, y, radix)
        countAdd = countAdd + answer[1]
        countMult = countMult + answer[2]
        return(answer[0], countAdd, countMult)

    m = math.ceil(n / 2)  # m = n / 2 if n is even, m = n / 2 + 1 if n is odd

    trailing_zeros_y = n - m  # nr of 0's
    countAdd += 1
    trailing_zeros_x = trailing_zeros_y * 2  # nr of 0's
    countMult += 1

    a = x[:m]  # split x into the upper digits
    b = x[m:]  # and the lower digits

    c = y[:m]  # same for y
    d = y[m:]

    ac = compute_karatsuba(a, c, radix, countAdd,
                           countMult)  # recurse to find a*c
    countAdd = ac[1]
    countMult = ac[2]
    ac = ac[0]

    bd = compute_karatsuba(b, d, radix, countAdd,
                           countMult)  # recurse to find b*d
    countAdd = bd[1]
    countMult = bd[2]
    bd = bd[0]

    xsum = add(a, b, radix)  # a + b
    countAdd += 1
    ysum = add(c, d, radix)  # c + d
    countAdd += 1

    # recurse to find (a+b)*(c+d)
    e = compute_karatsuba(xsum, ysum, radix, countAdd, countMult)
    countAdd = e[1]
    countMult = e[2]
    e = e[0]

    # remove leading 0's before subtraction otherwise the subtraction function crashes
    # remember the number of leading zero's removed, to add them later
    ac_lead_0_nr = ac.count("0")
    if ac.count("0") == len(ac):    # if ac only contains 0's
        ac_lead_0_nr -= 1           # nr of removed 0's is 1 less
    ac = remove_leading_zeros(ac)

    # remove leading 0's from bd
    bd_lead_0_nr = bd.count("0")
    if bd.count("0") == len(bd):    # if bd only contains 0's
        bd_lead_0_nr -= 1           # nr of removed 0's is 1 less
    bd = remove_leading_zeros(bd)

    e = subtract(e, ac, radix)  # compute e = (a+b)*(c+d) - ac
    countAdd += 1

    e = subtract(e, bd, radix)  # compute e = (a+b)*(c+d) - ac - bd
    countAdd += 1

    # if length of result from subtraction is smaller than the number of leading 0's that were removed
    # add the extra 0's back onto e as leading 0's
    # otherwise the length of the fragment is wrong
    if len(e) < max(ac_lead_0_nr, bd_lead_0_nr):
        e = "0" * max(ac_lead_0_nr, bd_lead_0_nr) + e

    # add trailing 0's
    ac = ac + '0' * trailing_zeros_x
    e = e + '0' * trailing_zeros_y

    result = add(ac, e, radix)
    countAdd += 1

    result = add(result, bd, radix)
    countAdd += 1

    result = remove_leading_zeros(result)   # remove leading 0's from result

    return (result, countAdd, countMult)

def display_poly(mod, f):
  poly = f[1:len(f)-1].split(',')  
  output = []
  for i in range(len(poly)):
    power = len(poly) - i - 1
    n = modular_reduction(poly[i] if poly[i] != '' else '0', mod, 10)
    if poly[i] and int(n) != 0:
      if power == 0:
        output.append(n)
        continue
      if power == 1:
        output.append((n if int(n) != 1 else '') + 'X')
        continue
      output.append((n if int(n) != 1 else '') + 'X^%s' % (power))

  
  # If it is only a constant polynomial
  if len(output) <= 1:
    if len(output) == 0 or output[0] == '':
      return 0
    else:
      return output[0]
  
  # Else
  return '+'.join(output)
