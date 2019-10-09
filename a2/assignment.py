
import math
from functions import *

input_file = open('input.txt', 'r').read().split('\n')
output = []
currentComputationLine = math.inf

def compute(input):
    # print(len(input))
    data = parseInput(input)
    method = getMethod(data)

    ans = None
    if method == 'display-poly':
        ans = display_poly(data['mod'], data['f'])
    elif method == 'add-poly':
        ans = display_poly(data['mod'], add_poly(data['mod'], data['f'], data['g']))
    elif method == 'subtract-poly':
        ans = display_poly(data['mod'], subtract_poly(data['mod'], data['f'], data['g']))
    elif method == 'multiply-poly':
        ans = display_poly(data['mod'], multiply_poly(data['mod'], data['f'], data['g']))
    elif method == 'long-div-poly':
        q, r = long_div_poly(data['mod'], data['f'], data['g'])
        data['computed-answ-q'] = q if q.startswith('ERROR') else display_poly(data['mod'], q)
        data['computed-answ-r'] = r if r.startswith('ERROR') else display_poly(data['mod'], r)
    elif method == 'euclid-poly':
        a, b, d = euclid_poly(data['mod'], data['f'], data['g'])
        data['computed-answ-a'] = display_poly(data['mod'], a)
        data['computed-answ-b'] = display_poly(data['mod'], b)
        data['computed-answ-d'] = display_poly(data['mod'], d)
    elif method == 'equals-poly-mod':
        ans = 'TRUE' if equals_poly_mod(data['mod'], data['f'], data['g'], data['h']) else 'FALSE'
    elif method == 'irreducible':
        ans = 'TRUE' if irreducible(data['mod'], data['f']) else 'FALSE'
    elif method == 'find-irred':
        ans = find_irred(data['mod'], data['deg'])
    else:
        return None
    
    if ans:
        data['computed-answer'] = ans

    return parseOutput(data)

for i in range(len(input_file)):
    line = input_file[i]

    if line.startswith('#'):
        continue
    if line.startswith('[mod]'):
        currentComputationLine = i
        continue

    if (i + 1) == len(input_file):
        compute(input_file[currentComputationLine:i+1])
        break
    
    if not input_file[i+1].strip() and currentComputationLine < math.inf:
        # All the information of the computation is between lines currentComputationLine and i
        result = compute(input_file[currentComputationLine:i+1])
        if result:
            output.append(result)
        currentComputationLine = math.inf

# Write it to the file
with open('output.txt', 'w') as output_file:
    output_file.write('\n'.join(output))

print("\033[1;37;42m The script has succesfully finished, take a look in the output.txt file! \033[0m")
