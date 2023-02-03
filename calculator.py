# write your code here
import re

# operators set
OPERATORS = {'+', '-', '*', '/'}


def check_command(s):
    if s == '/exit':
        print('Bye!')
        quit()
    elif s == '/help':
        print('The program calculates the sum of numbers')
    else:
        print('Unknown command')


def check_valid(s):
    s = s.replace(' ', '')
    for i in s:
        if i.isalpha():
            return True
    if s[-1] in OPERATORS:
        return True
    template = r'(([+-])*([0-9])+){1,}'
    if not re.match(template, s):
        return True
    return False


def calculate(s):

    while '-+' in s or '--' in s or '+-' in s or '++' in s:
        if '-+' in s:
            s = s.replace('-+', '-')
        if '--' in s:
            s = s.replace('--', '+')
        if '+-' in s:
            s = s.replace('+-', '-')
        if '++' in s:
            s = s.replace('++', '+')

    nums = s.split()
    res = int(nums[0])
    for i in range(1, len(nums)):
        if nums[i] == '+':
            res += int(nums[i + 1])
        if nums[i] == '-':
            res -= int(nums[i + 1])

    return res


def main():
    while True:
        user_input = input().strip(' ')
        if user_input == '':
            continue
        elif user_input.startswith('/'):
            check_command(user_input)
        else:
            if check_valid(user_input):
                print('Invalid expression')
            else:
                res = calculate(user_input)
                print(res)


if __name__ == '__main__':
    main()
