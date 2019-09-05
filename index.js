const fs = require('fs');
const convertHexToNumber = {
  0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, a: 10, b: 11, c: 12, d: 13, e: 14, f: 15
};
const convertNumberToHex = {
  0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'
};

try {
  const readFile = process.argv[2];
  const data = fs.readFileSync(readFile, 'utf8').split('\n');
  let output = [];

  
  let currentComputationLine = 0;

  // Loop through the file line by line
  for (let i = 0; i < data.length; i++) {
    let line = data[i];

    if (line[0] == "#") {
      continue;
    }
    if (line.startsWith("[radix]")) {
      // New computation, get all the data needed
      currentComputationLine = i;
    }

    // If the next line is a newline, then we have all the data 
    // we need for the current computation between
    // currentComputationLine and i
    if (i + 1 == data.length) {
      if (currentComputationLine !== Infinity) {
        let outputBlock = calculate(data.slice(currentComputationLine, i));
        !!outputBlock ? output.push(outputBlock) : null;
      }
      break;
    }
    if (data[i + 1].startsWith("\r") || data[i+1].startsWith("\n")) {
      let outputBlock = calculate(data.slice(currentComputationLine, i + 1));
      !!outputBlock ? output.push(outputBlock) : null;
      currentComputationLine = Infinity;
    }
  }

  // console.log(output)
  fs.writeFileSync('output.txt', output.join('\r'));

} catch (err) {
  console.error(err);
}



function calculate(input) {
  let data = parseInputBlock(input);

  // Check what method we need to use the input arguments for
  let method = '';
  for (option in data) {
    if (data[option] == '') {
      method = option;
    }
  }

  // Let's start calculating the output
  switch (method) {
    case 'add':
      data['computed-answer'] = add(parseInt(data.radix), data.x, data.y);
      break;
    case 'subtract':
      data['computed-answer'] = subtract(parseInt(data.radix), data.x, data.y);
      break;
    default:
      return '';
      // console.log(`Method ${method} is not supported.`);
      break;
  }

  return serializeOutputBlock(data);
}


function parseInputBlock(input) {
  let data = {};

  // Go through all of the arguments of this computation
  for (let i = 0; i < input.length; i++) {
    let line = input[i].replace(/[\n\r]/g, '');
    let [argument, n] = line.split('[')[1].split(']');
    data[argument] = n.trim();
  }

  return data;
}


function serializeOutputBlock(input) {
  let output = '';
  
  for (argument in input) {
    output += `[${argument}] ${input[argument]}\r`;
  }

  return output;
}


function add(radix, x, y) {
  let answer = '';
  let carry = 0;
  
  for (let i = x.length - 1; i >= 0; i--) {
    let first = convertHexToNumber[x[i]];
    let second = convertHexToNumber[y[i]];
    let result = first + second + carry;
    carry = Math.floor(result / radix);
    result = result % radix;
    
    answer = convertNumberToHex[result] + answer;
  }
  
  if (carry > 0) {
    answer = convertNumberToHex[carry] + answer;
  }

  return answer;
}


function subtract(radix, x, y) {
  let answer = '';
  let carry = 0;
  
  for (let i = x.length - 1; i >= 0; i--) {
    let first = convertHexToNumber[x[i]];
    let second = convertHexToNumber[y[i]];
    let result = first - second + carry;
    carry = Math.floor(result / radix);
    result = ((result % radix) + radix) % radix;

    answer = convertNumberToHex[result] + answer;
  }
  
  // If the number becomes negative after subtraction
  if (carry < 0) {
    answer = answer.split('');
    answer[answer.length - 1] = parseInt(answer[answer.length - 1]) - 1;
    for (let i = 0; i < answer.length; i++) {
      answer[i] = convertNumberToHex[15 - convertHexToNumber[answer[i]]];
    }
    answer = `-${answer.join('')}`;
  }

  // Remove leading zeroes
  answer = answer.replace(/^0+/, '');

  return answer;
}