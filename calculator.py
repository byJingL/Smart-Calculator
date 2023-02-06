# write your code here
import re

# operators set
OPERATORS = {'+', '-', '*', '/', '(', ')'}
variable_dict = {}


def check_command(s):
    if s == '/exit':
        print('Bye!')
        quit()
    elif s == '/help':
        print('The program calculates the sum of numbers')
    else:
        print('Unknown command')


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


def check_assignment(s):
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


def handle_multi_operations(s):
    while '-+' in s or '--' in s or '+-' in s or '++' in s:
        if '-+' in s:
            s = s.replace('-+', '-')
        if '--' in s:
            s = s.replace('--', '+')
        if '+-' in s:
            s = s.replace('+-', '-')
        if '++' in s:
            s = s.replace('++', '+')
    return s


def split_expression(s):
    s = s.replace(' ', '')
    new_s = s[0]

    for i in s[1:]:
        if i.isalnum():
            new_s += i
        else:
            new_s += f' {i} '

    e_list = new_s.split()
    return e_list


def check_expression_valid(e_list):
    # start
    if e_list[0] in {'*', '/', ')'}:
        print("Invalid expression")
        return False
    # end
    if e_list[0] in {'+', '-', '*', '/', '('}:
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


def calculate(e_list):
    if e_list[0].isdigit():
        res = int(e_list[0])
    else:
        res = int(variable_dict[e_list[0]])
    for i in range(len(e_list) - 1):
        if e_list[i] == '+':
            if e_list[i + 1].isdigit():
                res += int(e_list[i + 1])
            else:
                res += int(variable_dict[e_list[i + 1]])
        if e_list[i] == '-':
            if e_list[i + 1].isdigit():
                res -= int(e_list[i + 1])
            else:
                res -= int(variable_dict[e_list[i + 1]])

    return res


def main():

    while True:
        user_input = input().strip(' ')

        if user_input == '':
            continue

        # command
        if user_input.startswith('/'):
            check_command(user_input)

        elif '=' in user_input:
            check_assignment(user_input)

        # no operations, show the value
        elif all(i not in user_input for i in OPERATORS):
            show_value(user_input)

        # do calculation
        else:
            s = handle_multi_operations(user_input)
            expression_list = split_expression(s)

            if check_expression_valid(expression_list):
                res = calculate(expression_list)
                print(res)


if __name__ == '__main__':
    main()
