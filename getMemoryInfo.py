#!/usr/bin/python

import os

def getMemoryG(arg):
    res = 0.0
    if len(arg) == 0:
        return 0
    try:
        if arg[-1] == 'm':
            arg = arg.replace("m", "")
            res = float(arg)/1024
        elif arg[-1] == 'g':
            arg = arg.replace("g", "")
            res = float(arg)
        else:
            res = float(arg)/1024/1024
    except Exception, e:
        print "get memmory info error!!! Get the string is " + str(res)
        res = 0.0
    return res

#print getMemoryG("1024m")
#print getMemoryG("102400")
#print getMemoryG("1024g")

def getMemFromTop():
    command = "./getMemoryInfo.sh"
    memoryArg = os.popen(command).read().strip("\n").split('\n')
    return memoryArg

#print getMemoryArg()

def getMemGInfo():
    memSum = 0.0
    mem = getMemFromTop()
    for m in mem:
        #print m
        memSum += getMemoryG(m)
    res = memSum/len(mem)
    #print "res is " + str(res)
    return res

#print getMemGInfo()
