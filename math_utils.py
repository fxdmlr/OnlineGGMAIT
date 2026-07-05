import math
import cmath
import console_utils as cu
import random


MAX_ITER = 1000
MAX_ERR = 0.001

def heaviside(t):
    if t > 0:
        return 1
    else:
        return 0

class poly:
    def __init__(self, coeffs):
        self.coeffs = coeffs#[i.real if int(i.real) - float(i.real) != 0 else int(i.real) for i in coeffs]
        self.deg = len(coeffs) - 1
    
    def __call__(self, x):
        s = 0
        for i in range(len(self.coeffs)):
            s += self.coeffs[i] * x ** i
        
        return s
    
    def __add__(self, other):
        if isinstance(other, poly):
            if self.deg > other.deg:
                new_p = self.coeffs[:]
                for i in range(len(other.coeffs)):
                    new_p[i] += other.coeffs[i]
                
                return poly(new_p)
            
            else:
                new_p = other.coeffs[:]
                for i in range(len(self.coeffs)):
                    new_p[i] += self.coeffs[i]
                
                return poly(new_p)
        
        elif isinstance(other, (int, float)):
            np = self.coeffs[:]
            np[0] += other
            return poly(np)
    
    def __mul__(self, other):
        if isinstance(other, poly):
            p = [0 for i in range(len(self.coeffs) + len(other.coeffs) - 1)]
            for i in range(len(self.coeffs)):
                for j in range(len(other.coeffs)):
                    p[i + j] += self.coeffs[i] * other.coeffs[j]
            
            return poly(p[:])
        
        elif isinstance(other, (int, float)):
            return poly([other * i for i in self.coeffs[:]])
    
    def __neg__(self):
        return poly([-i for i in self.coeffs])
    
    def __sub__(self, other):
        return self + (-other)
    
    def __pow__(self, other):
        if isinstance(other, int):
            p = poly([1])
            for i in range(other):
                p *= self
            return p
    def __eq__(self, other):
        if not isinstance(other, poly):
            return False
        return self.coeffs[:] == other.coeffs[:]
    
    def __truediv__(self, other):
        def normalize(poly):
            while poly and poly[-1] == 0:
                poly.pop()
            if poly == []:
                poly.append(0)


        def poly_divmod(num, den):
            #Create normalized copies of the args
            num = num[:]
            normalize(num)
            den = den[:]
            normalize(den)

            if len(num) >= len(den):
                #Shift den towards right so it's the same degree as num
                shiftlen = len(num) - len(den)
                den = [0] * shiftlen + den
            else:
                return [0], num

            quot = []
            divisor = float(den[-1])
            for i in range(shiftlen + 1):
                #Get the next coefficient of the quotient.
                mult = num[-1] / divisor
                quot = [mult] + quot

                #Subtract mult * den from num, but don't bother if mult == 0
                #Note that when i==0, mult!=0; so quot is automatically normalized.
                if mult != 0:
                    d = [mult * u for u in den]
                    num = [u - v for u, v in zip(num, d)]

                num.pop()
                den.pop(0)

            normalize(num)
            return quot, num
        return poly(poly_divmod(self.coeffs[:], other.coeffs)[0])
    
    def __mod__(self, other):
        def normalize(poly):
            while poly and poly[-1] == 0:
                poly.pop()
            if poly == []:
                poly.append(0)


        def poly_divmod(num, den):
            #Create normalized copies of the args
            num = num[:]
            normalize(num)
            den = den[:]
            normalize(den)

            if len(num) >= len(den):
                #Shift den towards right so it's the same degree as num
                shiftlen = len(num) - len(den)
                den = [0] * shiftlen + den
            else:
                return [0], num

            quot = []
            divisor = float(den[-1])
            for i in range(shiftlen + 1):
                #Get the next coefficient of the quotient.
                mult = num[-1] / divisor
                quot = [mult] + quot

                #Subtract mult * den from num, but don't bother if mult == 0
                #Note that when i==0, mult!=0; so quot is automatically normalized.
                if mult != 0:
                    d = [mult * u for u in den]
                    num = [u - v for u, v in zip(num, d)]

                num.pop()
                den.pop(0)

            normalize(num)
            return quot, num
        return poly(poly_divmod(self.coeffs[:], other.coeffs)[1])

    def __round__(self, ndigits = 3):
        return poly([round(i, ndigits=ndigits) for i in self.coeffs])

    
    def pprint(self, prev_ppr = [[" "], ["x"]]):
        if all([i == 0 for i in self.coeffs]):
            return [[" "], ["0"]]
        
        arr = []
        for i in self.coeffs:
            r, c = i.real, i.imag
            if c == 0:
                if int(r) - r == 0:
                    arr.append(int(r))
                else:
                    arr.append(r)
            else:
                if int(r) - r == 0:
                    nr = int(r)
                else:
                    nr = r
                if int(c) - c == 0:
                    nc = int(c)
                else:
                    nc = c
                
                arr.append(complex(nr, nc))
        
        coeffs = arr[:]
        
        if not isinstance(coeffs[0], complex):
            if coeffs[0] < 0:
                sgn_ppr = [[" "], ["-"]]
            else:
                sgn_ppr = [[" "], ["+"]]
        else:
            sgn_ppr = [[" "], ["+"]]
            
        if self.coeffs[0] != 0:
            if isinstance(coeffs[0], complex):
                ppr = cu.connect_pprint(sgn_ppr, [[" " for i in str(coeffs[0])], [i for i in str(coeffs[0])]])
            else:
                ppr = cu.connect_pprint(sgn_ppr, [[" " for i in str(abs(coeffs[0]))], [i for i in str(abs(coeffs[0]))]])
        else:
            ppr = [[""], [""]]
        if len(coeffs) >= 2:
            if coeffs[1] != 0:
                if not isinstance(coeffs[1], complex):
                    if coeffs[1] < 0:
                        sgn_ppr = [[" "], ["-"]]
                    else:
                        sgn_ppr = [[" "], ["+"]]
                else:
                    sgn_ppr = [[" "], ["+"]]
                    
                sub = prev_ppr[:]
                if abs(coeffs[1]) != 1:
                    if isinstance(coeffs[1], complex):
                        coeff_ppr = [[" " for j in str(coeffs[1])], [j for j in str(coeffs[1])]]
                    else:
                        coeff_ppr = [[" " for j in str(abs(coeffs[1]))], [j for j in str(abs(coeffs[1]))]]
                else:
                    coeff_ppr = [[""], [""]]
                    
                sub3 = cu.connect_pprint(sgn_ppr, cu.connect_pprint(coeff_ppr, sub))
                
                ppr = cu.connect_pprint(sub3[:], ppr)
                
        for i in range(2, len(coeffs)):
            if coeffs[i] != 0:
                if not isinstance(coeffs[i], complex):
                    if coeffs[i] < 0:
                        sgn_ppr = [[" "], ["-"]]
                    else:
                        sgn_ppr = [[" "], ["+"]]
                else:
                    sgn_ppr = [[" "], ["+"]]
                    
                sub = cu.connect_pprint(prev_ppr[:], [[j for j in str(i)], [" " for j in str(i)]])
                if abs(coeffs[i]) != 1:
                    if isinstance(coeffs[i], complex):
                        coeff_ppr = [[" " for j in str(coeffs[i])], [j for j in str(coeffs[i])]]
                    else:
                        coeff_ppr = [[" " for j in str(abs(coeffs[i]))], [j for j in str(abs(coeffs[i]))]]
                else:
                    coeff_ppr = [[""], [""]]
                    
                sub3 = cu.connect_pprint(sgn_ppr, cu.connect_pprint(coeff_ppr, sub))
                
                ppr = cu.connect_pprint(sub3[:], ppr)
        
        return ppr
    
    def delete_excess_zeros(self):
        if len(self.coeffs) == 0:
            return
        i = len(self.coeffs[:]) - 1
        k = i + 1
        while self.coeffs[i] == 0 and i > 0:
            k = i
            i -= 1
        
        self.coeffs = self.coeffs[:k]
        
    
    def roots(self, prevs=[]):
        if len(self.coeffs) == 0:
            return prevs[:]
        if len(self.coeffs) == 1:
            return prevs[:]
        if self.coeffs[-1] == 0:
            return poly(self.coeffs[:-1]).roots(prevs=prevs[:])
        if self.coeffs[0] == 0:
            return poly(self.coeffs[1:]).roots(prevs=prevs[:] + [0])
        if self.deg == 1:
            return [-self.coeffs[0] / self.coeffs[1]] + prevs[:]
        
        if self.deg == 2:
            a = self.coeffs[2]
            b = self.coeffs[1]
            c = self.coeffs[0]
            d = b**2 - 4*a*c
            if a == 0:
                return poly(self.coeffs[:-1])
            return [(-b + cmath.sqrt(d))/(2*a), (-b - cmath.sqrt(d))/(2*a)] + prevs[:]
        
        if self.deg == 3:
            a = self.coeffs[3]
            b = self.coeffs[2]
            c = self.coeffs[1]
            d = self.coeffs[0]
            
            d0 = b**2 - 3*a*c
            d1 = 2*b**3-9*a*b*c+27*d*a**2
            if d0 == d1 == 0:
                r1 = (-1/(3*a)) * (b)
                r2, r3 = (self / poly([-r1, 1])).roots()
                return [r1, r2, r3] + prevs[:]
                
            C = ((d1 + cmath.sqrt(d1**2-4*d0**3)) / 2)**(1/3)
            if C == 0:
                C = ((d1 - cmath.sqrt(d1**2-4*d0**3)) / 2)**(1/3)
            
            if a == 0:
                return poly(self.coeffs[:-1]).roots()
            r1 = (-1/(3*a)) * (b + C + d0/C)
            r2, r3 = (self / poly([-r1, 1])).roots()
            
            return [r1, r2, r3] + prevs[:]
        
        if self.deg == 4:
            A = self.coeffs[4]
            B = self.coeffs[3]
            C = self.coeffs[2]
            D = self.coeffs[1]
            E = self.coeffs[0]
            a = -3*B**2/(8*A**2) + C/A
            b =  B**3/(8*A**3) - B*C/(2*A**2) + D/A
            c = -3*B**4/(256*A**4)+ C*B**2/(16*A**3) - B*D/(4*A**2)+ E/A
            d = -B / (4*A)
            #depressed_quartic = [c, b, a, 0, 1]
            if b == 0:
                r1 = cmath.sqrt(-a/2 + 0.5*cmath.sqrt(a**2-4*c))
                r2 = cmath.sqrt(-a/2 - 0.5*cmath.sqrt(a**2-4*c))
                r3 = -cmath.sqrt(-a/2 + 0.5*cmath.sqrt(a**2-4*c))
                r4 = -cmath.sqrt(-a/2 - 0.5*cmath.sqrt(a**2-4*c))
                
                return [r1+d, r2+d, r3+d, r4+d] + prevs[:]
            else:
                p = -a**2/12 - c
                q = -a**3/108+a*c/3-b**2/8
                w = (-q/2 + cmath.sqrt(q**2/4 + p**3/27))**(1/3)
                if w != 0:
                    y = a/6 + w-p/(3*w)
                else:
                    y = a/6
                r1 = 0.5*(-cmath.sqrt(2*y - a) + cmath.sqrt(-2*y-a+2*b/cmath.sqrt(2*y - a)))
                r2 = 0.5*(-cmath.sqrt(2*y - a) - cmath.sqrt(-2*y-a+2*b/cmath.sqrt(2*y - a)))
                r3 = 0.5*(cmath.sqrt(2*y - a) + cmath.sqrt(-2*y-a-2*b/cmath.sqrt(2*y - a)))
                r4 = 0.5*(cmath.sqrt(2*y - a) - cmath.sqrt(-2*y-a-2*b/cmath.sqrt(2*y - a)))
                return [r1+d, r2+d, r3+d, r4+d] + prevs[:]
        
        else:
            current = 0
            prev_root = current
            i = 0
            while True:
                if abs(prev_root - current) < MAX_ERR and i != 0:
                    break
                
                if i > MAX_ITER:
                    break
                
                prev_root = current
                d = self.diff()(current)
                if d != 0:
                    current -= self(current) / d
                else:
                    while self.diff()(current) == 0:
                        current += MAX_ERR
                    current -= self(current) / self.diff()(current)
                i += 1
            
            new_pol = self / (poly([-current, 1]))
            return new_pol.roots(prevs=prevs + [current])
        
            
    
    def diff(self):
        new_poly = [i * self.coeffs[i] for i in range(1, len(self.coeffs))]
        return poly(new_poly)
    
    def integrate(self):
        new_poly = [0]
        new_poly += [self.coeffs[i] / (i + 1) for i in range(len(self.coeffs))]
        return poly(new_poly)
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    @staticmethod
    def rand(deg, nranges=[-10, 10]):
        arr = [random.randint(nranges[0], nranges[1]) for i in range(deg + 1)]
        return poly(arr)


class ratexp:
    def __init__(self, num1, denom1):
        num = num1
        denom = denom1
        if isinstance(num1, poly):
            
            num1.delete_excess_zeros()
            num.delete_excess_zeros()
            if len(num1.coeffs) == 1:
                num = num1.coeffs[0] 
        if isinstance(denom1, poly):
            denom1.delete_excess_zeros()
            denom.delete_excess_zeros()
            if len(denom1.coeffs) == 1:
                denom = denom1.coeffs[0] 
                
        if isinstance(num, ratexp) and isinstance(denom, ratexp):
            self.num = num.num * denom.denom
            self.denom = num.denom * denom.num
        elif isinstance(num, ratexp):
            self.num = num.num
            self.denom = num.denom * denom
        elif isinstance(denom, ratexp):
            self.num = num * denom.denom
            self.denom = denom.num
        else:                
            self.num = num
            self.denom = denom
    
    def __call__(self, x):
        if callable(self.num):
            num = self.num(x)
        else:
            num = self.num
        
        if callable(self.denom):
            denom = self.denom(x)
        else:
            denom = self.denom
        
        return num / denom
    
    def simplify(self):
        #return self
        if isinstance(self.num, (int, float)):
            if isinstance(self.denom, (int, float)):
                return self.num / self.denom
            else:
                return self
        elif isinstance(self.denom, (int, float)):
            return self.num * (1/self.denom)
        
        else:
            #if self.num.deg > 4 or self.denom.deg > 4:
            #    return self

            num_root = self.num.roots()
            if num_root is None:
                return self
            if len(num_root) == 0:
                return self
            nroot_copy = num_root[:]
            denom_root = self.denom.roots()
            if denom_root is None:
                return self.num * (1 / self.denom)
            if len(denom_root) == 0:
                return self.num * (1 / self.denom)
            droot_copy = denom_root[:]
            cancelled = True
            
            while cancelled:
                broken = False
                for i in range(len(num_root)):
                    for j in range(len(denom_root)):
                        if num_root[i] == denom_root[j]:
                            num_root.pop(i)
                            denom_root.pop(j)
                            broken = True
                            break
                    if broken:
                        break
                else:
                    cancelled = False
            if num_root == nroot_copy and denom_root == droot_copy:
                return self
            np = self.num.coeffs[-1]
            nq = self.denom.coeffs[-1]
            
            for root in num_root:
                np *= poly([-root, 1])
            for root in denom_root:
                nq *= poly([-root, 1])
            
            return ratexp(np, nq)
    
    def pprint(self, prev_ppr=[[" "], ["x"]]):
        if isinstance(self.num, (int, float)):
            num_ppr = [
                [" " for i in str(self.num)],
                [i for i in str(self.num)]
            ]
        elif isinstance(self.num, poly):
            num_ppr = self.num.pprint(prev_ppr=prev_ppr)
        
        if isinstance(self.denom, (int, float)):
            denom_ppr = [
                [" " for i in str(self.denom)],
                [i for i in str(self.denom)]
            ]
        elif isinstance(self.denom, poly):
            denom_ppr = self.denom.pprint(prev_ppr=prev_ppr)
        
        mlen = max(len(denom_ppr[0]), len(num_ppr[0]))
        line = [["-" for i in range(mlen)]]
        
        n1_num = int((mlen - len(num_ppr[0])) / 2)
        n1_denom = int((mlen - len(denom_ppr[0])) / 2)
        new_num = num_ppr[:]
        for i in range(n1_num):
            num_ppr = cu.connect_pprint([[" "], [" "]], num_ppr[:])
        for i in range(mlen - n1_num):
            num_ppr = cu.connect_pprint(num_ppr[:], [[" "], [" "]])
        
        for i in range(n1_denom):
            denom_ppr = cu.connect_pprint([[" "], [" "]], denom_ppr[:])
        for i in range(mlen - n1_denom):
            denom_ppr = cu.connect_pprint(denom_ppr[:], [[" "], [" "]])
        
        return num_ppr + line + denom_ppr
    
    def __add__(self, other):
        if isinstance(other, ratexp):
            new_r = ratexp(self.num * other.denom + self.denom * other.num, self.denom * other.denom).simplify()
            return new_r
        
        elif isinstance(other, (poly, int, float)):
            new_r = ratexp(self.num + self.denom * other, self.denom).simplify()
            return new_r
    
    def __mul__(self, other):
        if isinstance(other, ratexp):
            new_r = ratexp(self.num * other.num, self.denom * other.denom).simplify()
            return new_r
        
        elif isinstance(other, (poly, int, float)):
            new_r = ratexp(self.num * other, self.denom).simplify()
            return new_r
    
    def __neg__(self):
        return ratexp(-self.num, self.denom).simplify()
    
    def __sub__(self, other):
        return self + (-other)
    
    def __truediv__(self, other):
        if isinstance(other, ratexp):
            new_r = ratexp(self.num * other.denom, self.denom * other.num).simplify()
            return new_r
        
        elif isinstance(other, (poly, int, float)):
            new_r = ratexp(self.num, self.denom * other).simplify()
            return new_r
    
    def __pow__(self, n):
        if n == 0:
            return 1
        if n == 1:
            return self
        else:
            p = ratexp(self.num, self.denom)
            for i in range(n - 1):
                p = p * self
            
            return p
    
    def diff(self):
        if isinstance(self.num, (int, float)) and isinstance(self.denom, (int, float)):
            return 0
        
        elif isinstance(self.num, (int, float)):
            return ratexp(-self.num * self.denom.diff(), self.denom * self.denom).simplify()
        
        elif isinstance(self.denom, (int, float)):
            return (self.num * (1/ self.denom)).diff()
        
        else:
            return ratexp(self.num.diff() * self.denom - self.num * self.denom.diff(), self.denom * self.denom).simplify()
    
    def ndiff(self, n):
        if n == 0:
            return self
        if n == 1:
            return self.diff()
        else:
            return self.diff().ndiff(n - 1)
    
    def partialfraction(self):
        if isinstance(self.denom, (int, float)):
            return None
        counted_array = []
        roots_array = self.denom.roots()
        lead_coeff = self.denom.coeffs[-1]
        keys = []
        for i in roots_array:
            if i not in keys:
                keys.append(i)
                counted_array.append([i, roots_array.count(i)])
        def find_coeffs(num, c_array, r, c, lead):
            new_denom = lead
            for root, count in c_array:
                if root != r:
                    new_denom *= poly([-root, 1]) ** count
            
            new_rat = ratexp(num, new_denom)
            coeff_arr = []
            for i in range(c):
                coeff_arr.append((new_rat.ndiff(i)(r)) / (math.factorial(i)))
            
            return coeff_arr[:]
        
        fin_arr = []
        for root, count in counted_array:
            fin_arr.append([root, find_coeffs(self.num, counted_array, root, count, lead_coeff)])
        
        return fin_arr[:]
    
    def integrate(self):
        z = 0
        if hasattr(self.num, 'deg') and hasattr(self.denom, 'deg'):
            if self.num.deg >= self.denom.deg:
                z = (self.num / self.denom).integrate()
                np = self.num % self.denom
            else:
                np = self.num
        elif hasattr(self.num, 'deg'):
            return self.simplify().integrate()
        elif hasattr(self.denom, 'deg'):
            np = self.num
        else:
            return poly([0, self.num / self.denom])
            
        pfd = ratexp(np, self.denom).partialfraction()
        arr = []
        for root, coeffs in pfd:
            sub = poly([-root, 1])
            for j in range(len(coeffs)):
                if j == 0:
                    arr.append([coeffs[j], log(sub)])
                else:
                    arr.append(ratexp(coeffs[j] / (-j), sub ** j))
        fin_arr = []
        for item in arr:
            if isinstance(item, list):
                fin_arr.append(mul([item[0].real if item[0].imag == 0 else item[0], item[1]]))
            else:
                fin_arr.append(item)
        if z != 0:
            return add([z] + fin_arr)   
        return add(fin_arr)
        
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    @staticmethod
    def rand(deg, nranges=[-10, 10]):
        p = poly.rand(random.randint(0, deg - 1), nranges=nranges)
        q = poly.rand(deg, nranges=nranges)
        return ratexp(p, q)

class log:
    def __init__(self, inp):
        self.inp = inp
    
    def __call__(self, x):
        if callable(self.inp):
            return cmath.log(self.inp(x))
        
        return cmath.log(self.inp)
    
    def pprint(self, prev_ppr=[[" "], ["x"]]):
        sub = [[' ' for i in range(4)], ['l', 'o', 'g', '(']]
        return cu.connect_pprint(sub, cu.connect_pprint(self.inp.pprint(prev_ppr=prev_ppr[:]), [[" "], [")"]]))
    
    def diff(self):
        if hasattr(self.inp, 'diff'):
            if isinstance(self.inp, ratexp):
                return (ratexp(self.inp.num.diff(), self.inp.num).simplify() - ratexp(self.inp.denom.diff(), self.inp.denom).simplify()).simplify()
            inp_diff = self.inp.diff().simplify() if hasattr(self.inp.diff(), 'simplify') else self.inp.diff()
            return ratexp(inp_diff, self.inp).simplify()
        else:
            return 0

class atan:
    def __init__(self, inp):
        self.inp = inp
    
    def __call__(self, x):
        if callable(self.inp):
            return cmath.atan(self.inp(x))
        
        return cmath.atan(self.inp)
    
    def pprint(self, prev_ppr=[[" "], ["x"]]):
        sub = [[" " for i in range(5)], ['a', 't', 'a', 'n', '(']]
        return cu.connect_pprint(sub, cu.connect_pprint(self.inp.pprint(prev_ppr=prev_ppr[:]), [[" 1"], [")"]]))
    
    def diff(self):
        if hasattr(self.inp, 'diff'):
            if isinstance(self.inp, ratexp):
                n = self.inp.num.diff() * self.inp.denom - self.inp.num * self.inp.denom.diff()
                d = self.inp.num ** 2 + self.inp.denom ** 2
                return ratexp(n, d).simplify()
            inp_diff = self.inp.diff().simplify() if hasattr(self.inp.diff(), 'simplify') else self.inp.diff()
            
            sub = (self.inp ** 2 + 1).simplify() if hasattr((self.inp ** 2 + 1), 'simplify') else (self.inp ** 2 + 1)

            return ratexp(inp_diff, sub).simplify()
        else:
            return 0

class add:
    def __init__(self, items):
        self.items = items[:]
    
    def __call__(self, x):
        s = 0
        for i in self.items:
            if callable(i):
                s += i(x)
            else:
                s += i
        
        return s
    
    def pprint(self, prev_ppr=[["x"]]):
        ppr = [[]]
        for item in self.items:
            if hasattr(item, 'pprint'):
                ppr = cu.connect_pprint(ppr, cu.connect_pprint([["+"]], item.pprint(prev_ppr=prev_ppr)))
            else:
                ppr = cu.connect_pprint(ppr, cu.connect_pprint([["+"]], [[i for i in str(item)]]))
        return ppr

class mul:
    def __init__(self, items):
        self.items = items[:]
    
    def __call__(self, x):
        s = 1
        for i in self.items:
            if callable(i):
                s *= i(x)
            else:
                s *= i
        
        return s
    
    def pprint(self, prev_ppr=[["x"]]):
        ppr = [[]]
        for item in self.items:
            if hasattr(item, 'pprint'):
                if isinstance(item, poly):
                    sub = cu.connect_pprint([["("]], cu.connect_pprint(item.pprint(prev_ppr=prev_ppr), [[")"]]))
                else:
                    sub = item.pprint(prev_ppr=prev_ppr)
                ppr = cu.connect_pprint(ppr, sub)
            else:
                ppr = cu.connect_pprint(ppr, [[i for i in str(item)]])
        return ppr

class matrix:
    def __init__(self, array):
        self.array = []
        for i in range(len(array)):
            sub = []
            for j in range(len(array[i])):
                if isinstance(array[i][j], (int, float)):
                    if abs(array[i][j] - int(array[i][j])) < 0.000001:
                        sub.append(int(array[i][j]))
                    else:
                        sub.append(array[i][j])
                else:
                    sub.append(array[i][j])
                
            self.array.append(sub[:])
    
    def __add__(self, other):
        if isinstance(other, (int, float, complex, poly)):
            new_mat = matrix.ones(len(self.array)) * other
            return self + new_mat
        
        new_array = [[self.array[i][j] + other.array[i][j] for j in range(len(self.array[i]))] for i in range(len(self.array))]
        return matrix(new_array)
    
    def __mul__(self, other):
        if isinstance(other, (int, float, complex, poly)):
            new_array = [[other * self.array[i][j] for j in range(len(self.array[i]))] for i in range(len(self.array))]
            return matrix(new_array)
        new_array = []
        for i in range(len(self.array)):
            
            row = []
            for j in range(len(other.array[i])):
                s = 0
                for k in range(len(self.array[i])):
                    s += self.array[i][k] * other.array[k][j]
                
                row.append(s)
            new_array.append(row)
        
        return matrix(new_array)
    
    def __neg__(self):
        return matrix([[-j for j in i] for i in self.array])
    
    def __sub__(self, other):
        return self + (-other)
    
    def __pow__(self, n):
        if n == 0:
            return matrix.ones(len(self.array))
        else:
            p = self
            for i in range(n - 1):
                p = p * self
            
            return p
    
    def det(self):
        if len(self.array) == 1:
            return self.array[0][0]
        else:
            s = 0
            for i in range(len(self.array[0])):
                new_array = []
                for j in range(1, len(self.array)):
                    sub = []
                    for k in range(len(self.array[j])):
                        if k != i :
                            sub.append(self.array[j][k])
                    
                    new_array.append(sub[:])
                
                s += matrix(new_array).det() * self.array[0][i] * ((-1)**i)
            
            return s
    
    def transpose(self):
        arr = [[0 for j in range(len(self.array))] for i in range(len(self.array[0]))]
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                arr[j][i] = self.array[i][j]
        
        return matrix(arr)
    
    def inverse(self):
        d = self.det()
        new_array = [[0 for j in range(len(self.array))] for i in range(len(self.array[0]))]
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                narr = []
                for k in range(len(self.array)):
                    if k == i:
                        continue
                    sub = []
                    for l in range(len(self.array[k])):
                        if l != j:
                            sub.append(self.array[k][l])
                    
                    narr.append(sub[:])
                
                if isinstance(d, (int, float, complex)):
                    new_array[j][i] = matrix(narr).det() * ((-1) ** (i + j)) * (1 / d)
                else:
                    new_array[j][i] = ratexp(matrix(narr).det() * ((-1) ** (i + j)), d).simplify()
        
        return matrix(new_array)
    
    def pprint(self, prev_ppr=[[" "], ["x"]]):
        tot_cells = []
        for i in self.array:
            cells = []
            for j in i:
                lines = [[], [], []]
                if hasattr(j, 'pprint'):
                    lines = cu.connect_pprint(lines, j.pprint(prev_ppr=prev_ppr[:]))
                else:
                    lines = cu.connect_pprint(lines, [[" " for i in range(len(str(j)))], [k for k in str(j)], [" " for i in range(len(str(j)))]])
                    
                cells.append(lines)
            
            tot_cells.append(cells)
        
        longest_length = 0
        for i in tot_cells:
            for j in i:
                if max([len(k) for k in j]) > longest_length:
                    longest_length = max([len(k) for k in j])
        tot_lines = []
        for i in range(len(tot_cells)):
            lines = [[], [], []]
            for j in range(len(tot_cells[i])):
               mlen = max([len(k) for k in tot_cells[i][j]])
               new_cell = cu.connect_pprint(tot_cells[i][j], [[" " for k in range((longest_length - mlen)//2)]for h in range(3)])
               new_cell2 = cu.connect_pprint([[" " for k in range((longest_length - mlen)//2 + (longest_length - mlen) % 2)]for h in range(3)], new_cell)
               lines = cu.connect_pprint(lines, new_cell2)
               if j != len(tot_cells[i]) - 1:
                   lines = cu.connect_pprint(lines, [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
                   
            tot_lines.append(lines)
        op = [[[" ", "_"], ["|", " "], ["|", " "]]] + [[["|", " "], ["|", " "], ["|", " "]] for i in range((len(tot_lines) - 2)*heaviside(len(tot_lines) - 2))] + [[["|", " "], ["|", " "], [" ", "-"]]]
        clsd = [[["_", " "], [" ", "|"], [" ", "|"]]] + [[[" ", "|"], [" ", "|"], [" ", "|"]] for i in range((len(tot_lines) - 2)*heaviside(len(tot_lines) - 2))] + [[[" ", "|"], [" ", "|"], ["-", " "]]]
        new_lines = []
        for i in range(len(tot_lines)):
            #print(lines[i])
            new_lines.append(cu.connect_pprint(op[i], cu.connect_pprint(tot_lines[i], clsd[i])))
        nl = []
        for i in new_lines:
            for j in i:
                nl.append(j)
        
        for i in range(len(nl)):
            if i == 0:
                mlen = len(nl[i])
            elif len(nl[i]) > mlen:
                mlen = len(nl[i])

        for i in range(len(nl)):
            ml = int((mlen - len(nl[i])) / 2)

            nl[i] = nl[i][:2] + [" " for j in range(ml)] + nl[i][2:len(nl[i]) - 2] +  [" " for j in range(mlen - ml - len(nl[i]))] + nl[i][len(nl[i]) - 2:]
        
        return nl
    
            
    def charpoly(self):
        return (matrix.ones(len(self.array)) * poly([0, 1]) - self).det()
                
    __rmul__ = __mul__
    __radd__ = __add__
    @staticmethod
    def randsq(n, nranges=[-10, 10], sgn=1):
        arr = [[abs(random.randint(nranges[0], nranges[1])) * ((-1) ** (random.randint(0, 1) * sgn)) for j in range(n)] for i in range(n)]
        return matrix(arr)
    
    @staticmethod
    def randsqpol(n, deg, nranges=[-10, 10]):
        arr = [[poly.rand(random.randint(0, deg), nranges=nranges) for j in range(n)] for i in range(n)]
        return matrix(arr)
    
    @staticmethod
    def ones(n):
        arr = [[int(i == j) for i in range(n)] for j in range(n)]
        return matrix(arr)
            
                


def NIntegrate(function, a, b, dx=0.01):
    s = 0
    pivot = a
    while pivot < b:
        s += function(pivot) * dx
        pivot += dx
    
    return s

def solve_linear_system(eq, lh):
    res = matrix(eq).inverse() * matrix([[i] for i in lh])
    return [i[0] for i in res.array]

