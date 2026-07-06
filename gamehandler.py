
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

def funMul(inpt_dict):
    ndig = int(inpt_dict['ndigits'])

    r = 0.7
    m1, m2 = random.randint(int(r*ndig), int(ndig / r)), random.randint(int(r*ndig), int(ndig / r)) 
    n1 = random.randint(10 ** (m1 - 1), 10 ** (m1) - 1)
    n2 = random.randint(10 ** (m2 - 1), 10 ** (m2) - 1)
    res = n1 * n2
    usr_inp = '%d * %d = '%(n1, n2)

    
    return usr_inp, str(res)

def ndigRand(m1):
    return random.randint(10 ** (m1 - 1), 10 ** (m1) - 1)

def ndigRandMat(dim, ndig):
    arr = [[ndigRand(ndig) for j in range(dim)] for i in range(dim)]
    return mu.matrix(arr)

def matMul(inpt_dict):
    dim = int(inpt_dict['dim'])
    num = int(inpt_dict['num'])
    ndig = int(inpt_dict['ndigits'])

    mat_arr = [mu.matrix([[ndigRand(ndig) for i in range(dim)]])] + [ndigRandMat(dim, ndig) for i in range(num)] + [mu.matrix([[ndigRand(ndig)] for i in range(dim)])] 
    res = mat_arr[0]
    ppr = mat_arr[0].pprint()
    for i in range(1, len(mat_arr)):
        ppr = cu.connect_pprint(ppr, mat_arr[i].pprint())
        res *= mat_arr[i]
    res = res.array[0][0]
    string = cu.strpprint(ppr) + "\n> "
    
    
    return string, str(res)
    



def introot(inpt_dict):
    ndig = int(inpt_dict['ndigits'])
    root = int(inpt_dict['n'])
    res = random.randint(math.ceil((10**(ndig - 1))**(1/root)), math.floor((10**(ndig))**(1/root)))
    num = res ** root
    rs = str(root)
    ns = str(num)
    if root == 2:
        string = " " + " " + "".join(["_" for i in ns]) + "\n" + "\\/"+ns + " = "
    
    
    else:
        string = rs + "".join(["_" for i in ns]) + "\n" + "\\/"+ns + " = "

    
    
    return string, str(res)

def regroot(inpt_dict):
    ndig = int(inpt_dict['ndigits'])
    root = int(inpt_dict['n'])
    resdig = int(inpt_dict['resdig'])
    num = random.randint(10**(ndig - 1), 10**(ndig))
    res = int(num ** (1/root) * (10 ** resdig)) / (10 ** resdig)#num ** (1/root)
    rs = str(root)
    ns = str(num)
    if root == 2:
        string = " " + " " + "".join(["_" for i in ns]) + "\n" + "\\/"+ns + " = "
    
    
    else:
        string = rs + "".join(["_" for i in ns]) + "\n" + "\\/"+ns + " = "
    
    
    return string, str(res)

def detgame(inpt_dict):
    dim = int(inpt_dict['dim'])
    ndigits = int(inpt_dict['ndigits'])
    a, b = 10 ** (ndigits - 1), 10 ** ndigits - 1
    mat = mu.matrix.randsq(dim, nranges=[a, b])
    res = mat.det()
    ppr = mat.pprint()
    ppr[0][0] = "|"
    ppr[0][1] = " "
    ppr[0][-1] = "|"
    ppr[0][-2] = " "
    ppr[-1][0] = "|"
    ppr[-1][1] = " "
    ppr[-1][-1] = "|"
    ppr[-1][-2] = " "
    ppr = cu.connect_pprint(ppr, [[" ", "=", " "]])
    string = "\n".join([''.join(i) for i in ppr]) + "\n"
    
    return string, str(res)

def regDiv(inpt_dict):
    ndig1 = int(inpt_dict['ndigitsnum'])
    ndig2 = int(inpt_dict['ndigitsdenom'])
    resdig = int(inpt_dict['resdig'])
    n1 = random.randint(10 ** (ndig1 - 1), 10 ** (ndig1) - 1)
    n2 = random.randint(10 ** (ndig2 - 1), 10 ** (ndig2) - 1)
    res = int(float(n1 / n2) * 10**resdig) / 10**resdig#n1 / n2
    string = '%d / %d = '%(n1, n2)

    
    return string, str(res)
