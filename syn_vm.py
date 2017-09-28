#!/usr/bin/python3

OPCODES = {}
OPCODES['HALT'] = 0
OPCODES['SET'] = 1
OPCODES['PUSH'] = 2
OPCODES['POP'] = 3
OPCODES['EQ'] = 4
OPCODES['GT'] = 5
OPCODES['JMP'] = 6
OPCODES['JT'] = 7
OPCODES['JF'] = 8
OPCODES['ADD'] = 9
OPCODES['MULT'] = 10
OPCODES['MOD'] = 11
OPCODES['AND'] = 12
OPCODES['OR'] = 13
OPCODES['NOT'] = 14
OPCODES['RMEM'] = 15
OPCODES['WMEM'] = 16
OPCODES['CALL'] = 17
OPCODES['RET'] = 18
OPCODES['OUT'] = 19
OPCODES['IN'] = 20
OPCODES['NOOP'] = 21

def load_val_operand(pc):
  word = int.from_bytes(memory[pc], 'little')
  if 0 <= word <= 32767:
    return word
  elif 32768 <= word <= 32775:
    return registers[word - 32768]
  else:
    print('Invalid value operand')
    exit()

def load_address_operand(pc):
  word = int.from_bytes(memory[pc], 'little')
  if 0 <= word <= 32767:
    address = word
  elif 32768 <= word <= 32775:
    address =  registers[word - 32768]
  else:
    print('Invalid address operand')
    exit()
  val = int.from_bytes(memory[address], 'little')
  return val

def save_register_operand(pc, value):
  word = int.from_bytes(memory[pc], 'little')
  if 32768 <= word <= 32775:
    registers[word - 32768] = value
  else:
    print('Invalid register operand')
    exit()

def save_address_operand(pc, value):
  word = int.from_bytes(memory[pc], 'little')
  if 0 <= word <= 32767:
    address = word
  elif 32768 <= word <= 32775:
    address =  registers[word - 32768]
  else:
    print('Invalid address operand')
    exit()
  save = value.to_bytes(2, 'little')
  memory[address] = save

registers = [0] * 8
memory = [bytes([0, 0]) for i in range(2**15)]
stack = list()

pc = 0

input_buf = ''

with open('challenge.bin', 'rb') as file:
  program = file.read()

# load program into memory
for i in range(0, len(program), 2):
  memory[i//2] = program[i : i+2]

while(True):
  opcode = int.from_bytes(memory[pc], 'little')
  if opcode == OPCODES['HALT']:
    print('Program terminated')
    exit()
  elif opcode == OPCODES['SET']:
    val = load_val_operand(pc+2)
    save_register_operand(pc+1, val)
    pc += 3
  elif opcode == OPCODES['PUSH']:
    val = load_val_operand(pc+1)
    stack.append(val)
    pc += 2
  elif opcode == OPCODES['POP']:
    if len(stack) == 0:
      print('Error: Pop operation cannot be performed on an empty stack')
      exit()
    val = stack.pop()
    save_register_operand(pc+1, val)
    pc += 2
  elif opcode == OPCODES['EQ']:
    a = load_val_operand(pc+2)
    b = load_val_operand(pc+3)
    if a == b:
      save_register_operand(pc+1, 1)
    else:
      save_register_operand(pc+1, 0)
    pc += 4
  elif opcode == OPCODES['GT']:
    a = load_val_operand(pc+2)
    b = load_val_operand(pc+3)
    if a > b:
      save_register_operand(pc+1, 1)
    else:
      save_register_operand(pc+1, 0)
    pc += 4
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
  elif opcode == OPCODES['ADD']:
    a = load_val_operand(pc+2)
    b = load_val_operand(pc+3)
    sum = (a + b) % 32768
    save_register_operand(pc+1, sum)
    pc += 4
  elif opcode == OPCODES['MULT']:
    a = load_val_operand(pc+2)
    b = load_val_operand(pc+3)
    prod = (a * b) % 32768
    save_register_operand(pc+1, prod)
    pc += 4
  elif opcode == OPCODES['MOD']:
    a = load_val_operand(pc+2)
    b = load_val_operand(pc+3)
    remain = a % b
    save_register_operand(pc+1, remain)
    pc += 4
  elif opcode == OPCODES['AND']:
    a = load_val_operand(pc+2).to_bytes(2, 'little')
    b = load_val_operand(pc+3).to_bytes(2, 'little')
    c = bytes([a[0] & b[0], a[1] & b[1]])
    ans = int.from_bytes(c, 'little')
    save_register_operand(pc+1, ans)
    pc += 4
  elif opcode == OPCODES['OR']:
    a = load_val_operand(pc+2).to_bytes(2, 'little')
    b = load_val_operand(pc+3).to_bytes(2, 'little')
    c = bytes([a[0] | b[0], a[1] | b[1]])
    ans = int.from_bytes(c, 'little')
    save_register_operand(pc+1, ans)
    pc += 4
  elif opcode == OPCODES['NOT']:
    a = load_val_operand(pc+2).to_bytes(2, 'little')

    b = bytes([~a[0] & 0xff, ~a[1] & 0x7f])
    ans = int.from_bytes(b, 'little')
    save_register_operand(pc+1, ans)
    pc += 3
  elif opcode == OPCODES['RMEM']:
    val = load_address_operand(pc+2)
    save_register_operand(pc+1, val)
    pc += 3
  elif opcode == OPCODES['WMEM']:
    val = load_val_operand(pc+2)
    save_address_operand(pc+1, val)
    pc += 3
  elif opcode == OPCODES['CALL']:
    address = pc + 2
    stack.append(address)
    jump = load_val_operand(pc+1)
    pc = jump
  elif opcode == OPCODES['RET']:
    if len(stack) == 0:
      print('Program terminated')
      exit()
    jump = stack.pop()
    pc = jump
  elif opcode == OPCODES['OUT']:
    ascii_val = load_val_operand(pc+1)
    print(chr(ascii_val), end='')
    pc += 2
  elif opcode == OPCODES['IN']:
    if len(input_buf) == 0:
      input_buf = input() + '\n'
    ascii_val = ord(input_buf[0])
    input_buf = input_buf[1:]
    save_register_operand(pc+1, ascii_val)
    pc += 2
  elif opcode == OPCODES['NOOP']:
    pc += 1
  else:
    print('Unrecognized opcode of value ' + str(opcode))
    exit()
