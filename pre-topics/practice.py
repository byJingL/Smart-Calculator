# ================ packing =================== #
my_tuple = 'hello', 123, [1,2,3]
print(type(my_tuple), my_tuple)

# ================ * operator =================== #
start, *middle, end = [1, 2, 3, 4, 5]
print(start)   # 1
print(end)     # 5
print(middle)  # [2, 3, 4]

# ================ use stack check brackets =================== #
from collections import deque

expression = '()5*()'
my_stack = deque()

for item in expression:
    if item == '(':
        my_stack.append('(')
    
    if item == ')':
        try:
            my_stack.pop()
        except IndexError:
            print('ERROR')
            quit()

if my_stack:
    print('ERROR')
else:
    print('OK')

# ================ Reversing a Queue =================== #
my_queue = deque()
my_queue.appendleft('a')
my_queue.appendleft('b')
my_queue.appendleft('c')
print(my_queue)  # deque(['c', 'b', 'a'])
reversed_queue = deque()
while my_queue:
    item = my_queue.pop()
    reversed_queue.append(item)
print(reversed_queue)  # deque(['a', 'b', 'c'])

my_stack = deque()
my_stack.append('0')
my_stack.append('1')

print(my_stack, my_stack[-1])

print('234'.isdigit())
print('234'.isnumeric())

import math
print(math.pow(5, 2))