def numbers_flout(num, numeral_system):
    """Переводит из 10-ной Ссч в другую (число дробное)"""
    system_numbers = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if numeral_system > len(system_numbers):
        return None
    num2 = float(num) - int(float(num))  # хранит дробную часть числа
    num1 = int(float(num))  # целая часть числа
    result_number = numbers_int(num1, numeral_system)  # переводит целую часть числа в другую Ссч
    result_float_number = ''
    limit = 0
    while num2 != 0 and limit <= 10:
        limit += 1
        result_float_number += system_numbers[int(num2 * numeral_system)]
        num2 = num2 * numeral_system - int(num2 * numeral_system)
    if isinstance(num, float):
        return f'{result_number}.{result_float_number}'
    return f'{result_number}'  # выводит как целое, так и дробное число


def numbers_int(number, numeral_system):
    """Переводит из 10-ной Ссч в другую (число целое)"""
    system_numbers = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
    return str(replace)