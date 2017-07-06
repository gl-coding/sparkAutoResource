#!/usr/bin/python

import scipy as sp

def getconfig():
    cpu = []
    memory  = []
    price   = []
    data = []
    pricefile = open('./pricefile.conf')
    lines = pricefile.readlines()
    for line in lines:
        tmp = line.strip("\n").split(',')
        #print tmp
        cpu.append(int(tmp[0]))
        memory.append(int(tmp[1]))
        price.append(float(tmp[2]))
    pricefile.close()

    data.append(cpu)
    data.append(memory)
    data.append(price)

    #print cpu
    #print memory
    #print price

    #print data
    return data

def floatEqual(arg0, arg1):
    diff = float(arg1) - float(arg1)
    if diff < 0.000001 and diff > -0.000001:
        return True
    return False

def selectDataCategory(data, arg):
    #print data
    #print data[2]
    res = []
    cpu_select = []
    memory_select = []
    price_select = []

    length = len(data[0])
    for val in range(0, length):
        print val
        cpu = data[0][val]
        memory = data[1][val]
        price = data[2][val]

        #print cpu
        #print memory
        #print price
        
        ratio = float(memory)/cpu

        diff = ratio - float(arg)
        if diff < 0.000001 and diff > -0.000001:
            print "equal"
            cpu_select.append(cpu)
            memory_select.append(memory)
            price_select.append(price)
        #print str(cpu) + " " + str(memory)
        
    res.append(cpu_select)
    res.append(memory_select)
    res.append(price_select)
    print res
    return res

def calTotalCost(num, price):
    return num*price

#get y = ax^3 + bx^2 + c, arguments is [a, b, c]
def getYval(arguments, x):
    res = 0.0
    length = len(arguments)
    for val in range(length):
        tmp = arguments[val]
        for v in range(length - 1 - val):
            tmp *= x
        res += tmp
    return res

#arguments = [1,1,1,1]
#y = 2x^2 + x + 1
#print getYval(arguments, 1)

def calAllConfCost(arguments, conf):
    args = arguments;
    res = []
    for val in conf:
        v = getYval(arguments, val)
        res.append(v)
    return res

#conf = [1,2,3]
#print calAllConfCost(arguments, conf)

#data = getconfig()
#selectDataCategory(data, 1)
#selectDataCategory(data, 2)
