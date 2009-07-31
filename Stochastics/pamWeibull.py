#!/usr/bin/env python
"""Quick hack to generate a Weibull distribution from a dataset"""

import sys, string, math, random

def drop_windows_newline(list):
    for i in range(len(list)):
        list[i] = list[i][:-2]
    return list

def make_float_of_string(list):
    for i in range(len(list)):
        list[i] = float(list[i])
    return list

class Stochastic:
    def __init__(self, list):
        if list: 
            self._list = list
            self._len = len(list)
        self._func = lambda x: x
        self._alpha = None
        self._beta = None
        self._gamma = None

    def Initialize(self):
        self._set_alpha()
        self._set_beta()
        self._set_gamma()
        
    def _sum(self, func=None, list=None):
        if not func: func = self._func
        if not list: list = self._list
        sum = 0
        for X in list:
            sum += func(X)
        return sum
        
    def _sum_squares(self, func=None, list=None):
        if not func: func = self._func
        if not list: list = self._list
        return self._sum(func=lambda x: math.pow(x,2))

    def _square_sums(self, func=None, list=None):
        if not func: func = self._func
        if not list: list = self._list
        sum = self._sum(func=func)
        return math.pow(sum,2)

    # Classes should over-ride these if necessary.
    def _set_alpha(self):
        pass
    def _set_beta(self):
        pass
    def _set_gamma(self):
        pass
        
class Exponential(Stochastic):
    def __init__(self, beta=None, list=None):
        Stochastic.__init__(self, list)
        if beta: self._beta = beta
        if list: self.Initialize()
        
    def Initialize(self):
        self._set_beta()
        
    def _set_beta(self):
        sum = self._sum(self._list)
        self._beta = sum/self._len
        

class Weibull(Stochastic):
    def __init__(self, alpha=None, beta=None, list=None):
        Stochastic.__init__(self, list)

        if alpha: self._alpha = alpha
        if beta: self._beta = beta
        if list: self.Initialize()

    def _set_alpha(self):
        self.__recursive_newton_iterator(iter=5)
        
    def _set_beta(self):
        sum = self._sum(func=lambda x: math.pow(x, self._alpha))
        result = sum/self._len
        power = 1/self._alpha
        self._beta = math.pow(result,power)

    def SetAlpha(self, alpha):
        self._alpha = alpha
    def SetBeta(self, beta):
        self._beta = beta

    def GetAlpha(self):
        return self._alpha
        
    def GetBeta(self):
        return self._beta
        
    def GetGamma(self):
        return self._gamma

    def GetA(self):
        sum = self._sum(func=lambda x: math.log(x))
        return sum/self._len
        
    def GetB(self):
        return self._sum(func=lambda x: math.pow(x, self._alpha))
        
    def GetC(self):
        return self._sum(func=lambda x: math.pow(x,self._alpha)*math.log(x))
    
    def GetH(self):
        return self._sum(func=lambda x: math.pow(x,self._alpha)*(math.pow(math.log(x),2)))
        
    def __recursive_newton_iterator(self, alpha=None, iter=4):
        if iter < 1: 
            return
        if not alpha: 
            alpha = self._alpha = self.__alpha_starter()
        A = self.GetA()
        B = self.GetB()
        C = self.GetC()
        H = self.GetH()
        numer = A + (1.0/alpha) - C/B
        denom = (B*H - math.pow(C,2))/math.pow(B,2) 
        denom += (1.0/math.pow(alpha,2))
        self._alpha = alpha + (numer/denom)
        iter -= 1
        self.__recursive_newton_iterator(self._alpha, iter)
    
    def __alpha_starter(self):
        outer = 6/(math.pow(math.pi,2))
        part1 = self._sum_squares(lambda x: math.log(x))
        part2 = self._square_sums(lambda x: math.log(x))
        inner = part1 - part2/self._len
        numer = outer*inner
        result = numer/(self._len-1)
        return math.sqrt(result)

    def __distribution(self, value):
        if value <= 0: return 0
        exp = -1.0*math.pow((value/self._beta),self._alpha)
        result = math.exp(exp)
        return 1.0 - result

    def __density(self, value):
        if value <= 0: return 0
        exp1 = -1.0 * self._alpha
        part1 = self._alpha * math.pow(self._beta,exp1)
        exp2 = self._alpha - 1.0
        part2 = math.pow(value, exp2)
        exp3 = -1.0 * (value/self._beta) * self._alpha
        part3 = math.exp(exp3)
        return part1 * part2 * part3
        
    def __probability(self, value):
        inside = -1.0 * math.log(value)
        exp = -1.0 * self._alpha
        return self._beta * math.pow(inside, exp)

    def Value(self, value):
        return self.__probability(value)
    
def RunSimulations():
    for i in range(1000):
        Q = wei.Value(random.random())
        k = random.uniform(0.00255271, 0.49523644)
        v = 50.0
        P = 10-((10 * k * v - Q) / (k * v))
        if P < 10: print "%1.5f" % P

datafile = '/home/john/data/hw_stochastic.txt'
#datafile = '/home/john/data/stochastic.data'
f = open(datafile, 'r')
lines = f.readlines()
lines = drop_windows_newline(lines)
lines = make_float_of_string(lines)

wei = Weibull(list=lines)
print wei.GetAlpha(), wei.GetBeta()
    
    