import math, re, random

#
#
#
#   ASSIGNMENT 1
#
#
#

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


#
#
#
#   ASSIGNMENT 2
#
#
#

########## start polynomial arithmetic ##########


# Parse string '{1,2,3}' into array ['1','2','3']
def polyToArray(poly):
    return poly[1:len(poly)-1].split(',')

# Parse array ['1','2','3'] into string '{1,2,3}'


def arrayToPoly(arr):
    return '{%s}' % (','.join(arr))

# Find the degree of a polynomial array from low to high power
# ['1', '2', '0] = 2X + 1 has degree 1


def degree(poly):
    while (len(poly) > 0 and int(poly[-1]) == 0):
        del poly[-1]
    return len(poly) - 1

# Get the leading coefficient of a polynomial array from low to high
# ['1', '2', '0] = 2X + 1 has lc 2


def lc(poly):
    for i in range(len(poly) - 1, -1, -1):
        if (int(poly[i]) > 0):
            return int(poly[i])
    return 0

# Function for parsing string '{1,2,3}' into polynomial "X^2+2X+3"


def display_poly(mod, f):
    poly = polyToArray(f)
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

# Function for adding two polynomials modulo m


def add_poly(mod, f, g):
    f = polyToArray(f)
    g = polyToArray(g)

    # add leading 0's to g or f so they are equal in length
    while (len(g) > len(f)):
        f = ['0'] + f
    while (len(f) > len(g)):
        g = ['0'] + g

    for i in range(len(f)):
        f[i] = modulo_add(f[i], g[i], mod, 10)
        # additional modular reduction necessary
        f[i] = modular_reduction(f[i], mod, 10)

    # remove leading 0's
    while f[0] == "0" and len(f) != 1:
        f.pop(0)

    return arrayToPoly(f)

# Function for subtracting two polynomials modulo m


def subtract_poly(mod, f, g):
    f = polyToArray(f)
    g = polyToArray(g)

    # add leading 0's to g or f so they are equal in length
    while (len(g) > len(f)):
        f = ['0'] + f
    while (len(f) > len(g)):
        g = ['0'] + g

    for i in range(len(f)):
        f[i] = modulo_subtract(f[i], g[i], mod, 10)
        f[i] = modular_reduction(f[i], mod, 10)

    # remove leading 0's
    while f[0] == "0" and len(f) != 1:
        f.pop(0)

    return arrayToPoly(f)

# Function for multiplication of two polynomials modulo m


def multiply_poly(mod, f, g):

    # Reverse polynomials X^2+3 => [3,0,1]
    f = polyToArray(f)[::-1]
    g = polyToArray(g)[::-1]

    # if either f or g is 0, return 0
    if f == "{0}" or g == "{0}":
        return "{0}"

    # initiate answer to array of size len(f)+len(g)-1
    ans = [0] * (len(f) + len(g) - 1)

    # Multiply every factor of both polynomials
    for i in range(len(f)):
        for j in range(len(g)):
            ans[i + j] = modulo_add(str(ans[i+j]),
                                    modulo_multiply(f[i], g[j], mod, 10), mod, 10)

    # remove leading 0's
    while ans[len(ans)-1] == "0" and len(ans) != 1:
        ans.pop()

    # take ans modulo mod
    for i in range(len(ans)):
        ans[i] = modular_reduction(ans[i], mod, 10)

    # Reverse the answer back and return it
    return arrayToPoly(ans[::-1])

# Function for long division of two polynomials modulo m


def long_div_poly(mod, f, g):

    poly_f = polyToArray(f)
    poly_g = polyToArray(g)

    # if length of f is smaller than length of g,
    # return quotient = 0 with f as remainder
    if len(poly_f) < len(poly_g):
        return ("{0}", arrayToPoly(poly_f))

    # return error if g = 0, division by 0 impossible
    if len(poly_g) == 1 and poly_g[0] == "0":
        return("ERROR", "ERROR")

    # return 0 if f = 0 -> 0/x = 0 for all x
    if len(poly_f) == 1 and poly_f[0] == "0":
        return("{0}", "{0}")

    rem = poly_f        # remainder
    quot = poly_g       # quotient

    for i in range(len(rem)):
        rem[i] = modular_reduction(rem[i], mod, 10)     # take remainder mod m
    for i in range(len(quot)):
        quot[i] = modular_reduction(quot[i], mod, 10)   # take quotient mod m

    r_deg = len(rem) - 1                        # degree of remainder
    q_deg = len(quot) - 1                       # degree of quotient

    # initiate output to empty list of size of largest degree difference + 1
    output = (r_deg - q_deg + 1)*[0]

    while r_deg >= q_deg:
        f_remain = []               # list for what's left of f after subtracting g
        g_min = quot                # preserve original g as we change it later on
        deg_diff = r_deg - q_deg    # recompute degree difference

        # increment output at correct position
        output[deg_diff] = output[deg_diff] + 1

        while deg_diff != 0:
            # append 0's to end of g to make g and f the same degree
            g_min.append("0")
            deg_diff -= 1       # change degree diff accordingly

        for j in range(r_deg + 1):
            # subtract the multiplied g from f
            f_remain.append(modulo_subtract(rem[j], g_min[j], mod, 10))

        rem = f_remain      # remainder = what remains of f after subtraction

        # loop continues forever if degree difference is 0
        # break loop if degree difference is 0 and remainder is 0
        if deg_diff == 0 and rem == ['0']:
            break

        # remove leading 0's from remainder
        if rem[0] == "0" and len(rem) != 1:
            rem.pop(0)
            r_deg = len(rem) - 1    # change degree of remainder

    output = output[::-1]   # reverse output list
    for i in range(len(output)):
        # take output elements modulo mod
        output[i] = output[i] % int(mod)
    # turn output elements into strings
    output = ''.join(str(e) for e in output)

    # remove leading 0's from remainder
    while rem[0] == "0" and len(rem) != 1:
            rem.pop(0)
    remainder = arrayToPoly(rem)    # turn remainder into string

    if remainder == '{}':         # if remainder is empty string
        remainder = "{0}"         # remainder = 0

    # return quotient and remainder
    return(arrayToPoly(output), remainder)

# Function for Extended Euclidean Algorithm for polynomials


def euclid_poly(mod, f, g):
    poly_f = polyToArray(f)
    poly_g = polyToArray(g)

    x = "{1}"
    v = "{1}"
    y = "{0}"
    u = "{0}"

    while poly_g != ["0"]:
        div = long_div_poly(mod, arrayToPoly(poly_f), arrayToPoly(poly_g))
        q = div[0]      # q = quotient (f / g)
        r = div[1]      # r = remainder (f / g)

        poly_f = poly_g                         # f = g
        poly_g = polyToArray(r)                 # g = r

        x_prime = x                             # x' = x
        y_prime = y                             # y' = y
        x = u                                   # x = u
        y = v                                   # y = v

        qu = multiply_poly(mod, q, u)          # calculate q*u
        u = subtract_poly(mod, x_prime,  qu)    # u = x' - q*u

        qv = multiply_poly(mod, q, v)           # calculate q*v
        v = subtract_poly(mod, y_prime,  qv)   # v = y' - q*v

    # calculate the inverse of lc(f) ---> lc(f)^-1
    inv_f = modular_inversion(poly_f[0], mod, 10)
    ans_a = multiply_poly(mod, x, arrayToPoly(
        inv_f.split()))     # ans_a = x * lc(f)^-1
    ans_b = multiply_poly(mod, y, arrayToPoly(
        inv_f.split()))     # ans_b = y * lc(f)^-1
    xf = multiply_poly(mod, ans_a, f)                               # x*f
    yg = multiply_poly(mod, ans_b, g)                               # y*g
    # x*f + y*g = gcd(f,g)
    ans_d = add_poly(mod, xf, yg)

    return ans_a, ans_b, ans_d

# Function for congruence modulo a polynomial
# ---> f - g = x*h for some x, equivalently, h | f - g


def equals_poly_mod(mod, f, g, h):

    poly_f = polyToArray(f)
    poly_g = polyToArray(g)
    poly_h = polyToArray(h)

    if poly_h == ['']:
        poly_h = ['0']

    for i in range(len(poly_f)):
        poly_f[i] = modular_reduction(poly_f[i], mod, 10)     # take f mod m
    for i in range(len(poly_g)):
        poly_g[i] = modular_reduction(poly_g[i], mod, 10)     # take g mod m
    for i in range(len(poly_h)):
        poly_h[i] = modular_reduction(poly_h[i], mod, 10)     # take h mod m

    difference = subtract_poly(mod, arrayToPoly(
        poly_f), arrayToPoly(poly_g))     # f - g
    divide = long_div_poly(mod, difference, arrayToPoly(
        poly_h))                  # (f - g) / h

    if divide[1] == '{0}':      # if ((f - g) / h) has 0 remainder
        return True             # true
    else:
        return False            # if not, false

# Function for testing if a polynomial is irreducible


def irreducible(mod, f):
    poly_f = polyToArray(f)

    if len(poly_f) == 1:    # degree of f must be at least 1
        return "ERROR"

    for i in range(len(poly_f)):
        poly_f[i] = modular_reduction(poly_f[i], mod, 10)     # take f mod m

    degree = len(poly_f) - 1            # degree of f
    mod_pow_deg = int(mod)**degree      # mod^(degree of f)

    poly_g = []

    # generate g: if f is irreducible, f divides g ->
    # f | X^(q^n)-X where q = mod and n = degree of f
    for i in range(mod_pow_deg, -1, -1):
        if i == mod_pow_deg:
            poly_g.append("1")
        elif i == 1:
            poly_g.append("-1")
        else:
            poly_g.append("0")

    divide = long_div_poly(mod, arrayToPoly(
        poly_g), arrayToPoly(poly_f))  # compute (g / f)

    if divide[1] == '{0}':      # if remainder is 0, return true
        return True
    else:
        return False

# Function for finding an irreducible polynomial given a degree and modulus


def find_irred(mod, deg):

    if deg == "0":      # degree must be at least 1
        return "ERROR"

    f_rndm = random_poly(mod, deg)  # generate random poly
    f = arrayToPoly(f_rndm)

    while irreducible(mod, f) == False:  # while random poly is not irreducible
        f_rndm = random_poly(mod, deg)  # generate new random poly
        f = arrayToPoly(f_rndm)

    return display_poly(mod, f)

# Function generates random polynomial with degree deg and numbers from 0 to mod-1,
# used by find_irred()


def random_poly(mod, deg):
    f = []
    for i in range(int(deg)+1):
        f.append(str(random.randint(0, int(mod)-1)))
    if f[0] == "0":
        f[0] = "1"
    return f

########## end polynomial arithmetic ##########


########## start finite field arithmetic ##########

def add_table(mod, mod_poly):
    pass


def mult_table(mod, mod_poly):
    pass


def display_field(mod, mod_poly, a):
    pass


def add_field(mod, mod_poly, a, b):
    pass


def subtract_field(mod, mod_poly, a, b):
    pass


def multiply_field(mod, mod_poly, a, b):
    pass


def inverse_field(mod, mod_poly, a):
    pass


def division_field(mod, mod_poly, a, b):
    pass


def equals_field(mod, mod_poly, a, b):
    pass


def primitive(mod, mod_poly, a):
    pass


def find_prim(mod, mod_poly):
    pass

########## end finite field arithmetic ##########
