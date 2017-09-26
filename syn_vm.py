#!/usr/bin/python3

OPCODES = {}
OPCODES['HALT'] = 0
OPCODES['JMP'] = 6
OPCODES['JT'] = 7
OPCODES['JF'] = 8
OPCODES['OUT'] = 19
OPCODES['NOOP'] = 21

def load_val_operand(pc):
  word = int.from_bytes(memory[pc], byteorder='little')
  if 0 <= word <= 32767:
    return word
  elif 32768 <= word <= 32775:
    return registers[word - 32768]
  else:
    print('Invalid value operand')
    exit()

registers = [0] * 8
memory = [bytes([0, 0]) for i in range(2**15)]
stack = list()

pc = 0

with open('challenge.bin', 'rb') as file:
  program = file.read()

# load program into memory
for i in range(0, len(program), 2):
  memory[i//2] = program[i : i+2]

while(True):
  opcode = int.from_bytes(memory[pc], byteorder='little')
  if opcode == OPCODES['HALT']:
    print('Program terminated')
    exit()
  elif opcode == OPCODES['JMP']:
    jump = load_val_operand(pc+1)
    pc = jump
  elif opcode == OPCODES['JT']:
    check = load_val_operand(pc+1)
    jump = load_val_operand(pc+2)
    if check != 0:
      pc = jump
    else:
      pc += 3
  elif opcode == OPCODES['JF']:
    check = load_val_operand(pc+1)
    jump = load_val_operand(pc+2)
    if check == 0:
      pc = jump
    else:
      pc += 3
  elif opcode == OPCODES['OUT']:
    ascii_val = load_val_operand(pc+1)
    print(chr(ascii_val), end='')
    pc += 2
  elif opcode == OPCODES['NOOP']:
    pc += 1
  else:
    print('Unrecognized opcode of value ' + str(opcode))
    exit()
  
# todo: write functions for retrieving value operands, address operands, and register operands
# todo: write functions for saving above operand types
