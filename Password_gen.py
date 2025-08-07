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
    # Спец знаки и цифры
    if is_num and is_spec:
        for i in range(length):
            str += alphabet[rn.randint(0,len(alphabet)-1)]
        if (not(re.search(alphabet_num,str))) and ((not(re.search(alphabet_spec,str)))):
            str = ""
            for j in range(length-1):
                str += alphabet[rn.randint(0,len(alphabet)-1)]
    # Цифры
    elif ((is_num == True) and (is_spec == False)):
        chars_0 = alphabet_word + alphabet_num
        for i in range(length):
            str += chars_0[rn.randint(0,len(chars_0)-1)]
        while bool(re.search(alphabet_spec, str)):
            str = ""
            for i in range(length):
                str += chars_0[rn.randint(0, len(chars_0) - 1)]
    elif ((is_num == False) and (is_spec == True)):
        chars_1 = alphabet_word + alphabet_spec
        for i in range(length):
            str += chars_1[rn.randint(0,len(chars_1)-1)]
        while bool(re.search(alphabet_num, str)) and (bool(re.search(alphabet_spec, str)) == False):
            str = ""
            for i in range(length):
                str += chars_1[rn.randint(0, len(chars_1) - 1)]
    # Todo: fix branch
    return str, bool(re.search(alphabet_spec, str))

print(pass_gen(10,False,True))