'''
Each problem is an object with these methods :

rand : to generate a random problem of that sub-genre
solution : to solve this instance of the problem returning a number
pprint : returns the pprint of the problem.
'''


import math_utils as mu
import console_utils as cu
import cmath
import random


class RationalIntegral:
    def __init__(self, rat, bounds):
        self.rat = rat
        self.bounds = bounds
    
    def solution(self):
        f = self.rat.integrate()
        return (f(self.bounds[1]) - f(self.bounds[0])).real
    
    def pprint(self):
        func_ppr = self.rat.pprint()
        integral_sign = [
            ["/"],
            ["|"],
            ["|"],
            ["|"],
            ["/"]
        ]
        mlen_bounds = max(len(str(self.bounds[1])), len(str(self.bounds[0])))
        bounds = [[i for i in str(self.bounds[1])] + [" " for i in range(mlen_bounds - len(str(self.bounds[1])))] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [i for i in str(self.bounds[0])] + [" " for i in range(mlen_bounds - len(str(self.bounds[0])))] + [" "]]
        fin = cu.connect_pprint(integral_sign, cu.connect_pprint(bounds, cu.connect_pprint(func_ppr, [[" ", "d", "x"]])))
        return fin
    
    @staticmethod
    def rand(deg=5, nranges=[-10, 10], boundary_ranges = [-10, 10], boundary_length_ranges = [1, 10]):
        a = random.randint(boundary_ranges[0], boundary_ranges[1])
        b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
        obj = RationalIntegral(mu.ratexp.rand(deg, nranges=nranges), [a, b])
        while True:
            try:
                s = obj.solution()
                return obj
            except:
                a = random.randint(boundary_ranges[0], boundary_ranges[1])
                b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
                obj = RationalIntegral(mu.ratexp.rand(deg, nranges=nranges), [a, b])

class PolyIntegral:
    def __init__(self, p, bounds):
        self.p = p
        self.bounds = bounds
    
    def solution(self):
        f = self.p.integrate()
        return (f(self.bounds[1]) - f(self.bounds[0]))
    
    def pprint(self):
        func_ppr = self.p.pprint()
        integral_sign = [
            ["/"],
            ["|"],
            ["|"],
            ["|"],
            ["/"]
        ]
        mlen_bounds = max(len(str(self.bounds[1])), len(str(self.bounds[0])))
        bounds = [[i for i in str(self.bounds[1])] + [" " for i in range(mlen_bounds - len(str(self.bounds[1])))] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [i for i in str(self.bounds[0])] + [" " for i in range(mlen_bounds - len(str(self.bounds[0])))] + [" "]]
        fin = cu.connect_pprint(integral_sign, cu.connect_pprint(bounds, cu.connect_pprint(func_ppr, [[" " for i in range(3)], [" ", "d", "x"]])))
        return fin
    
    @staticmethod
    def rand(deg=5, nranges=[-10, 10], boundary_ranges = [-10, 10], boundary_length_ranges = [1, 10]):
        a = random.randint(boundary_ranges[0], boundary_ranges[1])
        b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
        obj = PolyIntegral(mu.poly.rand(deg, nranges=nranges), [a, b])
        while True:
            try:
                s = obj.solution()
                return obj
            except:
                a = random.randint(boundary_ranges[0], boundary_ranges[1])
                b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
                obj = PolyIntegral(mu.poly.rand(deg, nranges=nranges), [a, b])

class PolyLogIntegral:
    def __init__(self, p, q, bounds):
        # Integral for p(x)log(q(x))
        self.p = p
        self.q = q
        self.bounds = bounds
    
    def solution(self):
        p = self.p.integrate()
        r = mu.ratexp(self.q.diff() * p, self.q).simplify().integrate()
        f = lambda x : p(x) * mu.log(self.q)(x) - r(x)
        return (f(self.bounds[1]) - f(self.bounds[0])).real

    def pprint(self):
        func_ppr = cu.connect_pprint([[" "], ["("]], cu.connect_pprint(self.p.pprint(), [[" "], [")"]]))
        func_ppr = cu.connect_pprint(func_ppr, mu.log(self.q).pprint())
        integral_sign = [
            ["/"],
            ["|"],
            ["|"],
            ["/"]
        ]
        mlen_bounds = max(len(str(self.bounds[1])), len(str(self.bounds[0])))
        bounds = [[i for i in str(self.bounds[1])] + [" " for i in range(mlen_bounds - len(str(self.bounds[1])))] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [i for i in str(self.bounds[0])] + [" " for i in range(mlen_bounds - len(str(self.bounds[0])))] + [" "]]
        fin = cu.connect_pprint(integral_sign, cu.connect_pprint(bounds, cu.connect_pprint(func_ppr, [[" " for i in range(3)], [" ", "d", "x"]])))
        return fin
    
    @staticmethod
    def rand(deg=1, nranges=[-10, 10], boundary_ranges = [-10, 10], boundary_length_ranges = [1, 10]):
        a = random.randint(boundary_ranges[0], boundary_ranges[1])
        b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
        obj = PolyLogIntegral(mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), [a, b])
        while True:
            try:
                s = obj.solution()
                return obj
            except:
                a = random.randint(boundary_ranges[0], boundary_ranges[1])
                b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
                obj = PolyLogIntegral(mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), [a, b])
                
class PolyAtanIntegral:
    def __init__(self, p, q, bounds):
        # Integral for p(x)atan(q(x))
        self.p = p
        self.q = q
        self.bounds = bounds
    
    def solution(self):
        p = self.p.integrate()
        r = (mu.atan(self.q).diff() * p).simplify().integrate()
        f = lambda x : p(x) * mu.atan(self.q)(x) - r(x)
        return (f(self.bounds[1]) - f(self.bounds[0])).real
    
    def adiff(self):
        p = self.p.integrate()
        r = (mu.atan(self.q).diff() * p).simplify().integrate()
        f = lambda x : p(x) * mu.atan(self.q)(x) - r(x)
        return f
    
    def pprint(self):
        func_ppr = cu.connect_pprint([[" "], ["("]], cu.connect_pprint(self.p.pprint(), [[" "], [")"]]))
        func_ppr = cu.connect_pprint(func_ppr, mu.atan(self.q).pprint())
        integral_sign = [
            ["/"],
            ["|"],
            ["|"],
            ["/"]
        ]
        mlen_bounds = max(len(str(self.bounds[1])), len(str(self.bounds[0])))
        bounds = [[i for i in str(self.bounds[1])] + [" " for i in range(mlen_bounds - len(str(self.bounds[1])))] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [i for i in str(self.bounds[0])] + [" " for i in range(mlen_bounds - len(str(self.bounds[0])))] + [" "]]
        fin = cu.connect_pprint(integral_sign, cu.connect_pprint(bounds, cu.connect_pprint(func_ppr, [[" " for i in range(3)], [" ", "d", "x"]])))
        return fin
    
    @staticmethod
    def rand(deg=1, nranges=[-10, 10], boundary_ranges = [-10, 10], boundary_length_ranges = [1, 10]):
        a = random.randint(boundary_ranges[0], boundary_ranges[1])
        b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
        obj = PolyAtanIntegral(mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), [a, b])
        while True:
            try:
                s = obj.solution()
                return obj
            except:
                a = random.randint(boundary_ranges[0], boundary_ranges[1])
                b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
                obj = PolyAtanIntegral(mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), [a, b])


class QuadExpIntegral:
    def __init__(self, p, q, r, s, quad, bounds):
        '''
        Integrates (p + q*sqrt(quad)) / (r + s*sqrt(quad))
        '''
        self.p = p
        self.q = q
        self.r = r
        self.s = s
        self.quad = quad
        self.bounds = bounds
    
    def solution(self):
        f = lambda x : (self.p(x) + self.q(x) * cmath.sqrt(self.quad(x))) / (self.r(x) + self.s(x) * cmath.sqrt(self.quad(x)))
        return mu.NIntegrate(f, self.bounds[0], self.bounds[1])
    
    def pprint(self):
        nquad_ppr = [["_" for i in self.quad.pprint()[0]]] + self.quad.pprint()
        sq_ppr = cu.connect_pprint([[" ", " ", " "], [" ", " ", "/"], ["\\", "/", " "]], nquad_ppr)
        p_ppr = [[" " for i in self.p.pprint()[0]]] + self.p.pprint()
        q_ppr = [[" " for i in self.q.pprint()[0]]] + self.q.pprint()
        r_ppr = [[" " for i in self.r.pprint()[0]]] + self.r.pprint()
        s_ppr = [[" " for i in self.s.pprint()[0]]] + self.s.pprint()
        num_ppr = cu.connect_pprint(p_ppr, cu.connect_pprint([[" ", " "], [" ", " "], ["+", "("]], cu.connect_pprint(cu.connect_pprint(q_ppr, [[" ", " "], [" ", " "], [" ", ")"]]), sq_ppr)))
        denom_ppr = cu.connect_pprint(r_ppr, cu.connect_pprint([[" ", " "], [" ", " "], ["+", "("]], cu.connect_pprint(cu.connect_pprint(s_ppr, [[" ", " "], [" ", " "], [" ", ")"]]), sq_ppr)))
        line = [["-" for i in range(max(len(num_ppr[0]), len(denom_ppr[0])))]]
        func_ppr = num_ppr + line + denom_ppr
        
        integral_sign = [
            ["/"],
            ["|"],
            ["|"],
            ["/"]
        ]
        mlen_bounds = max(len(str(self.bounds[1])), len(str(self.bounds[0])))
        bounds = [[i for i in str(self.bounds[1])] + [" " for i in range(mlen_bounds - len(str(self.bounds[1])))] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [" " for i in range(mlen_bounds)] + [" "],
                  [i for i in str(self.bounds[0])] + [" " for i in range(mlen_bounds - len(str(self.bounds[0])))] + [" "]]
        fin = cu.connect_pprint(integral_sign, cu.connect_pprint(bounds, cu.connect_pprint(func_ppr, [[" " for i in range(3)], [" ", "d", "x"]])))
        return fin
    
    @staticmethod
    def rand(deg=2, nranges=[-10, 10], boundary_ranges=[-10, 10], boundary_length_ranges=[1, 10]):
        p, q, r, s, quad = mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), mu.poly.rand(2, nranges=nranges)
        a = random.randint(boundary_ranges[0], boundary_ranges[1])
        b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
        obj = QuadExpIntegral(p, q, r, s, quad, [a, b])
        while True:
            try:
                s = obj.solution()
                return obj
            except:
                p, q, r, s, quad = mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), mu.poly.rand(deg, nranges=nranges), mu.poly.rand(2, nranges=nranges)
                a = random.randint(boundary_ranges[0], boundary_ranges[1])
                b = a + random.randint(boundary_length_ranges[0], boundary_length_ranges[1])
                obj = QuadExpIntegral(p, q, r, s, quad, [a, b])


