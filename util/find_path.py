#!/usr/bin/python3

# nodes are represented as a list of possible next steps
# steps are represented as (operation, operand, next_node)

nodes = [[('+', 4, 4), ('+', 4, 2), ('-', 4, 2), ('-', 9, 1)],     # node 0
         [('-', 4, 2), ('-', 11, 5), ('-', 18, 3), ('*', 18, 3)],  # node 1
         [('+', 4, 4), ('*', 4, 4), ('*', 8, 6), ('*', 11, 5), 
          ('-', 11, 5), ('-', 18, 3), ('-', 9, 1)],                # node 2
         [('-', 9, 1), ('-', 11, 5), ('-', 4, 2), ('*', 11, 5), 
          ('*', 1, 7), ('*', 9, 1)],                               # node 3
         [('*', 8, 6), ('*', 11, 5), ('*', 4, 2), ('+', 4, 2)],    # node 4
         [('*', 4, 2), ('*', 4, 4), ('*', 8, 6), ('-', 8, 6), 
          ('-', 1, 7), ('*', 1, 7), ('*', 18, 3), ('-', 4, 2),
          ('-', 9, 1), ('-', 18, 3)],                              # node 5
         [('*', 4, 4), ('-', 1, 7), ('-', 11, 5), ('*', 11, 5), 
          ('*', 4, 2), ('*', 4, 4)],                               # node 6
         []]                                                       # node 7

path = []

def find_path(cur_node, val, length):
  path.append((cur_node, val, length))
  if len(nodes[cur_node]) == 0 and val == 30:
    print("Success")
    print(path)
    exit()
  if length == 0:
    path.pop()
    return
  if val <= 0:
    path.pop()
    return
  if val > 1000000:
    path.pop()
    return
  for edge in nodes[cur_node]:
    operator, operand, next_node = edge
    if operator == '+':
      new_val = val + operand
      find_path(next_node, new_val, length - 1)
    if operator == '-':
      new_val = val - operand
      find_path(next_node, new_val, length - 1)
    if operator == '*':
      new_val = val * operand
      find_path(next_node, new_val, length - 1)
  path.pop()

for i in range(10):
  find_path(0, 22, i)
