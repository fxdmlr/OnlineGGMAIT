
import random
import math
import console_utils as cu
import math_utils as mu
import time


def organize_num_string(num, char=","):
    nstr = str(num)
    sub_str = ""
    for i in range(len(nstr)):
        sub_str += nstr[i]
        if not (len(nstr) - i - 1) % 3:
            sub_str += char
    return sub_str[:-1]

def regMul(inpt_dict):
    ndig = int(inpt_dict['ndigits'])
    n1 = random.randint(10 ** (ndig - 1), 10 ** (ndig) - 1)
    n2 = random.randint(10 ** (ndig - 1), 10 ** (ndig) - 1)
    res = n1 * n2
    
    return "%d * %d = "%(n1, n2), str(res)
