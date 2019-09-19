
import math

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

#function for addition (tested, works)
def add(x, y, radix):
    answer = ''
    carry = 0
    for i in range(len(x)-1,-1,-1):
        x_i = hexToNumber(x[i])
        y_i = hexToNumber(y[i])
        z_i = int(x_i) + int(y_i) + carry  
        carry = math.floor(z_i/radix)    
        z_i = z_i % radix
        answer = numberToHex(str(z_i)) + answer
    if carry > 0: 
        answer = numberToHex(str(carry)) + answer
    return answer

#function for subtraction (tested, works)
def subtract(x, y, radix):
    answer = ''
    carry = 0
    for i in range(len(x)-1,-1,-1):
        x_i = hexToNumber(x[i])
        y_i = hexToNumber(y[i])
        z_i = int(x_i) - int(y_i) + carry
        carry = math.floor(z_i/radix)    
        z_i = ((z_i % radix) + radix) % radix
        answer = numberToHex(str(z_i)) + answer
    #if number becomes negative after subtraction
    if carry < 0:
        answer = list(answer)
        answer[len(answer)-1] = int(answer[len(answer)-1]) - 1
        for i in range(0,len(answer)):
            answer[i] = numberToHex(str(15 - int(hexToNumber(answer[i]))))
        separator = ''
        answer = separator.join(answer)
        answer = '-' + answer
    #remove leading 0's
    answer = answer.lstrip("0")
    return answer
        
#function for multiplication (tested, works)
def multiply(x, y, radix):
    countAdd = 0
    countMult = 0
    answer = ["0"] * (len(x) + len(y)) 

    #check if numbers are negative
    negative = False
    if x[0] == '-':
        negative = not negative
        x = x[1:]
    if y[0] == '-':
        negative = not negative
        y = y[1:]
    # Reverse the strings, so the i and j are the same as in the algoritm 1.3 decription
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

            t = int(hexToNumber(answer[i+j])) + int(first) * int(second) + c
            countAdd = countAdd + 3
            countMult = countMult + 1

            c = math.floor(t/radix)
            countMult = countMult + 1

            answer[i+j] = numberToHex(str(t - c * radix))
            countAdd = countAdd + 2
            countMult = countMult + 1
            
        answer[i + len(y)] = str(numberToHex(c))
        countAdd = countAdd + 1
        for u in range(0,len(answer)):
            answer[u] = numberToHex(answer[u])

    k = len(x) + len(y)
    countAdd = countAdd + 1
    if answer[len(x) + len(y) - 1] == "0":
        k = k - 1
        countAdd = countAdd + 1
    countAdd = countAdd + 1

    answer = answer[0:k]
    answer.reverse()
    answer = ''.join(answer)

    if negative:
        answer = '-' + answer

    return (answer, countAdd, countMult)
