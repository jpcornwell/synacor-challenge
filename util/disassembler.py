#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()

OPCODE_TRACE_FMT = [None] * 22
OPCODE_TRACE_FMT[0] = 'HALT'
OPCODE_TRACE_FMT[1] = 'SET {} {}'
OPCODE_TRACE_FMT[2] = 'PUSH {}'
OPCODE_TRACE_FMT[3] = 'POP {}'
OPCODE_TRACE_FMT[4] = 'EQ {} {} {}'
OPCODE_TRACE_FMT[5] = 'GT {} {} {}'
OPCODE_TRACE_FMT[6] = 'JMP {}'
OPCODE_TRACE_FMT[7] = 'JT {} {}'
OPCODE_TRACE_FMT[8] = 'JF {} {}'
OPCODE_TRACE_FMT[9] = 'ADD {} {} {}'
OPCODE_TRACE_FMT[10] = 'MULT {} {} {}'
OPCODE_TRACE_FMT[11] = 'MOD {} {} {}'
OPCODE_TRACE_FMT[12] = 'AND {} {} {}'
OPCODE_TRACE_FMT[13] = 'OR {} {} {}'
OPCODE_TRACE_FMT[14] = 'NOT {} {}'
OPCODE_TRACE_FMT[15] = 'RMEM {} {}'
OPCODE_TRACE_FMT[16] = 'WMEM {} {}'
OPCODE_TRACE_FMT[17] = 'CALL {}'
OPCODE_TRACE_FMT[18] = 'RET'
OPCODE_TRACE_FMT[19] = 'OUT {}'
OPCODE_TRACE_FMT[20] = 'IN {}'
OPCODE_TRACE_FMT[21] = 'NOOP'

def print_operand(pc):
  if pc > len(memory) - 1:
    return ''

  word = int.from_bytes(memory[pc], 'little')
  if 0 <= word <= 32767:
    return str(word)
  elif 32768 <= word <= 32775:
    return 'R' + str(word - 32768)

memory = [bytes([0, 0]) for i in range(2**15)]
pc = 0

# load program into memory
with open(args.input, 'rb') as file:
  program = file.read()
for i in range(0, len(program), 2):
  memory[i//2] = program[i : i+2]

while True:
  opcode = int.from_bytes(memory[pc], 'little')

  if opcode >= 22: # uncrecognized opcode
    # I'm pretty sure this could actually cause incorrect results, but 
    # it seems to match up with the trace output
    print('Unknown')
    pc += 1
    continue

  out = ''
  # print the address of the opcode
  out += '${:<8}'.format(pc.to_bytes(2, 'little').hex())
  out += '${:<8}'.format(pc)

  # print the opcode
  out += OPCODE_TRACE_FMT[opcode].format(print_operand(pc+1),
                                         print_operand(pc+2),
                                         print_operand(pc+3))
  print(out)

  # count the number of operands and increment PC accordingly
  pc += OPCODE_TRACE_FMT[opcode].count('{}') + 1

  if pc > len(memory) - 1:
    exit()
