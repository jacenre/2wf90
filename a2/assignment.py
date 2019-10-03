
import math
from functions import *

input_file = open('input.txt', 'r').read().split('\n')
output = []
currentComputationLine = math.inf

def compute(input):
    # print(len(input))
    data = parseInput(input)
    method = getMethod(data)

    if method == 'display-poly':
        ans = display_poly(data['mod'], data['f'])
    elif method == 'add-poly':
        ans = display_poly(data['mod'], add_poly(data['mod'], data['f'], data['g']))
    elif method == 'subtract-poly':
        ans = display_poly(data['mod'], subtract_poly(data['mod'], data['f'], data['g']))
    else:
        return None
    
    data['computed'] = ans

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
