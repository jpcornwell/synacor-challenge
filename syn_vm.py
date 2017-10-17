#!/usr/bin/python3

import argparse
import shelve

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('-l', '--load', 
                    help='load virtual machine from a specific state (given via input option)', 
                    action='store_true')
parser.add_argument('-t', '--trace', 
                    help='create a trace of the program execution',
                    action='store_true')
parser.add_argument('-d', '--debug',
                    help='start syn-vm in debug mode',
                    action='store_true')
args = parser.parse_args()

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
  word = int.from_bytes(memory[pc], 'little')
  if 0 <= word <= 32767:
    return str(word)
  elif 32768 <= word <= 32775:
    return 'R' + str(word - 32768)

def get_opcode_format(pc):
  opcode = int.from_bytes(memory[pc], 'little')
  out = ''
  # print the address of the opcode
  out += '${:<8}'.format(pc.to_bytes(2, 'little').hex())
  out += '${:<8}'.format(pc)

  # print the opcode
  out += OPCODE_TRACE_FMT[opcode].format(print_operand(pc+1),
                                         print_operand(pc+2),
                                         print_operand(pc+3))
  return out

def print_trace(pc):
  out = get_opcode_format(pc)
  with open('trace.out', 'a') as trace:
    trace.write(out + '\n')

def print_debug(pc):
  out = get_opcode_format(pc)
  print(out + '\n')
    

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

def debug_menu():
  print('Registers (0-7): ' + str(registers))
  print('Stack: ' + str(stack))
  print('DEBUG> ', end='')
  command = input()
  if command == 'step' or command == '':
    return
  elif command == 'continue':
    global debug_break
    debug_break = False
    return
  elif command.startswith('break address'):
    command = command.split()
    debug_breakpoints.append(int(command[2]))
    debug_menu()
  elif command.startswith('remove break address'):
    command = command.split()
    debug_breakpoints.remove(int(command[3]))
    debug_menu()
  elif command.startswith('display breaks'):
    print('Breaks: ' + str(debug_breakpoints))
    debug_menu()
  elif command.startswith('set register'):
    command = command.split()
    registers[int(command[2])] = int(command[3])
    debug_menu()

registers = [0] * 8
memory = [bytes([0, 0]) for i in range(2**15)]
stack = list()
pc = 0
input_buf = ''

# load program into memory
if args.load == False:
  with open(args.input, 'rb') as file:
    program = file.read()

  for i in range(0, len(program), 2):
    memory[i//2] = program[i : i+2]

# load from state
if args.load == True:
  with shelve.open(args.input) as state:
    registers = state['registers']
    memory = state['memory']
    stack = state['stack']
    pc = state['pc']

# start a new trace if trace.out already exists and -t is specified
if args.trace == True:
  open('trace.out', 'w').close()

if args.debug == True:
  debug_break = True
  debug_breakpoints = []
else:
  debug_break = False

while(True):
  if args.trace == True:
    print_trace(pc)
  if args.debug == True:
    print_debug(pc)
    if pc in debug_breakpoints:
      debug_break = True
    if debug_break == True:
      debug_menu()
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
    if args.debug == True:
      with open('display.out', 'a') as display:
        display.write(chr(ascii_val))
    else:
      print(chr(ascii_val), end='')
    pc += 2
  elif opcode == OPCODES['IN']:
    if len(input_buf) == 0:
      print('INPUT> ', end='')
      input_buf = input() + '\n'

    # DEBUG
    if input_buf == 'debug: save\n':
      with shelve.open('state.out') as state:
        state['registers'] = registers
        state['memory'] = memory
        state['stack'] = stack
        state['pc'] = pc
      print('State has been saved')
      input_buf = ''
      continue
    # END DEBUG

    ascii_val = ord(input_buf[0])
    input_buf = input_buf[1:]
    save_register_operand(pc+1, ascii_val)
    pc += 2
  elif opcode == OPCODES['NOOP']:
    pc += 1
  else:
    print('Unrecognized opcode of value ' + str(opcode))
    exit()
