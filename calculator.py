# write your code here
import re
from collections import deque
import math


def check_command(s):
    if s == '/exit':
        print('Bye!')
        quit()
    elif s == '/help':
        print('The program calculates the sum of numbers')
    else:
        print('Unknown command')


def show_binary(s):
    s = s.replace(' ', '')
    if s[1:].isdigit():
        print(s)
    elif not s[1:].isalpha():  # alpha + num
        print("Invalid identifier")
    else:  # variable
        if s[1:] in variable_dict:
            print('-', variable_dict[s[1:]])
        else:
            print("Unknown variable")


def show_value(s):
    if " " in s:
        print("Invalid expression")
    elif s.isdigit():  # nums
        print(int(s))
    elif not s.isalpha():  # alpha + num
        print("Invalid identifier")
    else:  # variable
        if s in variable_dict:
            print(variable_dict[s])
        else:
            print("Unknown variable")


def do_assignment(s):
    if s.count('=') > 1:
        print("Invalid assignment")
    else:
        pattern = r"(\w+)\s*=\s*(-?\w+)"
        match = re.match(pattern, s)
        left = match.group(1)
        right = match.group(2)

        if not left.isalpha():
            print("Invalid identifier")
        else:
            try:
                variable_dict[left] = int(right)
            except ValueError:
                if right.isalpha():
                    # check existing variables
                    if right in variable_dict:
                        # match
                        variable_dict[left] = variable_dict[right]
                    else:
                        # not match
                        print("Unknown variable")
                else:
                    # invalid variable name
                    print("Invalid assignment")


def check_sequence(s):
    # not support sequence
    if any(i in s for i in NOT_SUPPORT_SEQUENCE):
        print("Invalid expression")
        return False

    return True


def handle_sequence_operation(s):
    while any(i in s for i in SUPPORT_SEQUENCE):
        if '-+' in s:
            s = s.replace('-+', '-')
        if '--' in s:
            s = s.replace('--', '+')
        if '+-' in s:
            s = s.replace('+-', '-')
        if '++' in s:
            s = s.replace('++', '+')
    return s


def check_parenthesis_valid(e_list):
    parenthesis_stack = deque()
    for item in e_list:
        if item == '(':
            parenthesis_stack.append('(')
        if item == ')':
            try:
                parenthesis_stack.pop()
            except IndexError:
                print('Invalid expression')
                return False
    if parenthesis_stack:
        print('Invalid expression')
        return False
    return True


def check_expression_valid(e_list):
    # start
    if e_list[0] in {'*', '/', ')'}:
        print("Invalid expression")
        return False
    # end
    if e_list[-1] in {'+', '-', '*', '/', '('}:
        print("Invalid expression")
        return False

    # variable
    for item in e_list:
        if item.isalnum() and (not item.isdigit()):
            pattern = r'(\w+)'
            if not re.match(pattern, item):
                print("Invalid identifier")
                return False
            else:
                if item not in variable_dict:
                    print("Unknown variable")
                    return False
    return True


def split_expression(s: str) -> list:
    s = s.replace(' ', '')

    if s[0] in OPERATORS:
        new_s = f'{s[0]} '
    else:
        new_s = s[0]

    for i in s[1:]:
        if i.isalnum():
            new_s += i
        else:
            new_s += f' {i} '

    e_list = new_s.split()
    return e_list


def infix_to_postfix(e_list: list) -> deque:
    stack = deque()
    result = deque()

    for item in e_list:
        # 1. Add operands (numbers and variables) to the result (postfix notation) as they arrive.
        if item not in OPERATORS:
            result.append(item)
        else:
            # 2. If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
            if not stack or stack[-1] == "(":
                stack.append(item)
            # 5. If the incoming element is a left parenthesis, push it on the stack.
            elif item == "(":
                stack.append(item)
            # 6. If the incoming element is a right parenthesis
            elif item == ")":
                # pop the stack and add operators to the result until you see a left parenthesis
                while stack[-1] != "(":
                    result.append(stack.pop())
                # Discard the pair of parentheses
                stack.pop()
            # 3. If the incoming operator has higher precedence than the top of the stack, push it on the stack
            elif (stack[-1] in LOW_OPERATORS and item in HIGH_OPERATORS) or \
                    (stack[-1] in HIGH_OPERATORS and item == '^') or (stack[-1] in LOW_OPERATORS and item == '^'):
                stack.append(item)
            # 4. If the precedence of the incoming operator is lower than or equal to that of the top of the stack
            else:
                # pop the stack and add operators to the result until
                # you see an operator that has smaller precedence or a left parenthesis on the top of the stack
                while stack and not \
                        ((stack[-1] in LOW_OPERATORS and item in HIGH_OPERATORS) or
                         (stack[-1] == "(") or (stack[-1] in HIGH_OPERATORS and item == '^') or
                         (stack[-1] in LOW_OPERATORS and item == '^')):
                    result.append(stack.pop())
                # then add the incoming operator to the stack.
                stack.append(item)
    # 7. At the end of the expression, pop the stack and add all operators to the result
    while stack:
        result.append(stack.pop())

    return result


def basic_cal(num1: float, num2: float, op: str) -> float:
    if op == '+':
        return int(num1 + num2)

    if op == '-':
        return int(num2 - num1)

    if op == '*':
        return num1 * num2

    if op == '/':
        return int(round(num2 / num1, 0))

    if op == '^':
        return int(math.pow(num2, num1))


def do_calculation(e_postfix: deque) -> int:
    res = deque()
    while e_postfix:
        item = e_postfix.popleft()

        if item.isdigit():
            res.append(float(item))
        if item.isalpha():
            res.append(float(variable_dict[item]))
        if item in OPERATORS:
            first = res.pop()
            second = res.pop()
            res.append(basic_cal(first, second, item))

    return int(res[-1])


# operators set
OPERATORS = {'+', '-', '*', '/', '(', ')', '^'}
SUPPORT_SEQUENCE = {'++', '--', '+-', '-+'}
NOT_SUPPORT_SEQUENCE = {'**', '//', '*/', '/*'}
HIGHEST_OPERATORS = {"^"}
HIGH_OPERATORS = {"*", "/", "(", ")"}
LOW_OPERATORS = {"+", "-"}
variable_dict = {}


def main():

    while True:
        user_input = input().strip(' ')

        if user_input == '':
            continue

        # command
        if user_input.startswith('/'):
            check_command(user_input)
        # do assignment
        elif '=' in user_input:
            do_assignment(user_input)
        # one binary input, show the value
        elif re.match(r'- *?\w+', user_input):
            show_binary(user_input)
        # no operations, show the value
        elif all(i not in user_input for i in OPERATORS):
            show_value(user_input)

        # do calculation
        else:
            if check_sequence(user_input):
                s = handle_sequence_operation(user_input)
                expression_list = split_expression(s)

                if check_expression_valid(expression_list) and check_parenthesis_valid(expression_list):
                    postfix = infix_to_postfix(expression_list)
                    res = do_calculation(postfix)
                    print(res)


if __name__ == '__main__':
    main()
