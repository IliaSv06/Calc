from variables import *


def numbers_flout(number, numeral_system):
    """Переводит из 10-ной Ссч в другую (число дробное)"""
    if numeral_system > len(system_numbers):
        return None
    number = abs(number) # число в модуле
    num2 = float(number) - int(float(number))  # хранит дробную часть числа
    num1 = int(float(number))  # целая часть числа
    result_number = numbers_int(num1, numeral_system)  # переводит целую часть числа в другую Ссч
    result_float_number = ''
    limit = 0
    while num2 != 0 and limit <= 10:
        limit += 1
        result_float_number += system_numbers[int(num2 * numeral_system)]
        num2 = num2 * numeral_system - int(num2 * numeral_system)
    if isinstance(number, float):
        return f'{result_number}.{result_float_number}0'
    return result_number


def numbers_int(number, numeral_system):
    """Переводит из 10-ной Ссч в другую (число целое)"""
    if number == 0:
        return '0'
    result_number = ''
    while number != 0:
        result_number = system_numbers[number % numeral_system] + result_number
        number = number // numeral_system
    return result_number


def numbers_10(number, q):
    """Переводит в 10-ную Ссч"""
    number = list(str(number))
    replace = 0
    n = len(number) - 1
    for i1 in number:
        if '.' in number:
            n = len(number[0:number.index('.')]) - 1
            number.remove('.')
        opiration = int(i1, 16) * (q ** n)
        replace += opiration
        n -= 1
    return replace

def conversion(number, notation_old: int, notation_new: int):
    """Переводит число из любой Ссч в другую Ссч"""
    x = numbers_10(number, notation_old)
    return numbers_flout(x, notation_new)

def conversion_expression(expression: str, notation_old: int= 10, notation_new: int = 10):
    """Переводит все числа в выражении в указанную Ссч"""
    if expression == '':
        return ''
    list_op = ['+', '-', '/', 'x', '*', ')']
    new_expression = ''
    number = ''
    for index in range(len(expression)):
        if all([expression[index] in list_op, expression[index -1] in system_numbers, index != 0, len(number) != 0]):
            new_expression += str(conversion(number, notation_old, notation_new))
            new_expression += expression[index]
            number = ''
        elif expression[index] in system_numbers:
            number += expression[index]
        else:
            new_expression += expression[index]
    if len(number) != 0:
        new_expression += str(conversion(number, notation_old, notation_new))
    return new_expression


def counting(expression: str, notation: int):
    """Считает выражение"""
    return eval(conversion_expression(expression, notation, 10))

