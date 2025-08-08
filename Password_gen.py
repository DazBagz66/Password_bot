import string
import random as rn
import re


def pass_gen(length, is_num, is_spec):

    str = ""
    alphabet_word = string.ascii_letters
    alphabet_num = string.digits
    alphabet_spec = ".&!?"
    alphabet = alphabet_num +  alphabet_spec + alphabet_word

    """ Ветвления """
    if is_num and is_spec:  # Спец знаки и цифры
         str = ""
         str += rn.choice(alphabet_spec) + rn.choice(alphabet_num)
         for i in range(length - 2):
             str += rn.choice(alphabet)
             str = ''.join(rn.sample(str,len(str)))
    elif ((is_num == True) and (is_spec == False)):  # Цифры
        chars_0 = alphabet_word + alphabet_num
        str = ""
        str += rn.choice(alphabet_num)
        for i in range(length - 1):
            str += rn.choice(chars_0)
            str = ''.join(rn.sample(str,len(str)))
    elif ((is_num == False) and (is_spec == True)):  # Спец знаки
        chars_0 = alphabet_word + alphabet_spec
        str = ""
        str += rn.choice(alphabet_num)
        for i in range(length - 1):
            str += rn.choice(chars_0)
            str = ''.join(rn.sample(str, len(str)))
    else:
        str = ""
        for i in range(length):
            str += alphabet_word[rn.randint(0, len(alphabet_word) - 1)]
    return str