#!/usr/bin/python3

# representation of node
# (operation, operand, next_node)

a = [[('+', 4, 4), ('+', 4, 2), ('-', 4, 2), ('-', 9, 1)],     # node 0
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

stack = []

def f(node, val, length):
  stack.append((node, val, length))
  if len(a[node]) == 0 and val == 30:
    print("Success")
    print(stack)
  if length == 0:
    stack.pop()
    return
  if val <= 0:
    stack.pop()
    return
  if val > 1000000:
    stack.pop()
    return
  for edge in a[node]:
    if edge[0] == '+':
      val2 = val + edge[1]
      f(edge[2], val2, length - 1)
    if edge[0] == '-':
      val2 = val - edge[1]
      f(edge[2], val2, length - 1)
    if edge[0] == '*':
      val2 = val * edge[1]
      f(edge[2], val2, length - 1)
  stack.pop()

f(0, 22, 6)

print('Done')
