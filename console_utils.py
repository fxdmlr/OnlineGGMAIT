def connect_pprint(ppr1, ppr2):
    if len(ppr1) > len(ppr2):
        sppr1 = ppr1[:]
        empty_line = [" " for i in range(len(ppr2[0]))]
        n1 = int((len(ppr1) - len(ppr2))/2)
        n2 = len(ppr1) - n1
        
        sppr2 = ppr2[:]
        for i in range(n1):
            sppr2 = [empty_line[:]] + sppr2[:]
        for i in range(n2):
            sppr2 = sppr2[:] + [empty_line[:]]
    
    else:
        sppr2 = ppr2[:]
        empty_line = [" " for i in range(len(ppr1[0]))]
        n1 = int((len(ppr2) - len(ppr1))/2)
        n2 = len(ppr2) - n1
        
        sppr1 = ppr1[:]
        for i in range(n1):
            sppr1 = [empty_line[:]] + sppr1[:]
        for i in range(n2):
            sppr1 = sppr1[:] + [empty_line[:]]
    
    new_ppr = []
    for i in range(min(len(sppr1), len(sppr2))):
        new_ppr.append(sppr1[i] + sppr2[i])
    
    return new_ppr

def strpprint(ppr):
    return "\n".join(["".join(i) for i in ppr])
