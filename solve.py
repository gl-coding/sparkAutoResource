#!/usr/bin/python

import numpy as np
import scipy as sp

def cal(x):
    res = x*x*x + x*x + x + 1
    print res


def genData(x0, y0, x1, y1, x2, y2, x3, y3):
    a = []
    tmp = [x0*x0*x0, x0*x0, x0, 1]
    a.append(tmp)
    tmp = [x1*x1*x1, x1*x1, x1, 1]
    a.append(tmp)
    tmp = [x2*x2*x2, x2*x2, x2, 1]
    a.append(tmp)
    tmp = [x3*x3*x3, x3*x3, x3, 1]
    a.append(tmp)

    b = [y0, y1, y2, y3]

    a = np.array(a)
    b = np.array(b)
    x = np.linalg.solve(a, b)
    print a
    print b
    print x
    
    a_ = x[0]*6
    b_ = x[1]*2

    point = -b_/(3*a_)

    print "point..."
    print point


#genData(1, 4, 2, 15, 3, 40, 4, 85)

a = [1, 2, 3, 4]
b = [4, 15, 40, 85]

fp = sp.polyfit(a, b, 3)

def genPoint(x0, y0, x1, y1, x2, y2, x3, y3):
    a = [x0, x1, x2, x3]

print fp



#cal(1)
#cal(2)
#cal(3)
#cal(4)


print ""
