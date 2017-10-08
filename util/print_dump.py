#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()

memory = [bytes([0, 0]) for i in range(2**15)]

# load program into memory
with open(args.input, 'rb') as file:
  program = file.read()

for i in range(0, len(program), 2):
  memory[i//2] = program[i : i+2]

print('Columns represent the following:')
print('Address represented as two byte little endian hex,')
print('Value of memory address represented as two byte little endian hex,')
print('Address represented as integer')
print('')
for address, word in enumerate(memory):
  print('${:<8} {:8} ${}'.format(address.to_bytes(2, 'little').hex(), 
                                 word.hex(), address))
