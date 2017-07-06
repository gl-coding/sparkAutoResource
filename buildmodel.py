#!/usr/bin/python

import mysql as ms
import scipy as sp

#res = ms.queryRuntimeInfo("BigDataBench Kmeans")

def stringToModel(string):
    l = []
    tmp = string.replace("[", "").replace("]", "").replace(" ", "").split(",")
    for val in tmp:
        l.append(float(val))
    return l

#print stringToModel("[1, 2, 3]")

def getCalPoints(arg):
    a = []
    b = []
    res = []
    for i in range(len(arg)):
        a.append(float(arg[i][0]))
        b.append(float(arg[i][1]))
    res.append(a)
    res.append(b)
    #print res
    return res

#pos = getCalPoints(res)

def getArgument(points):
    #print points
    x = points[0]
    y = points[1]

    fp = sp.polyfit(x, y, 3)
    res = []
    for val in fp:
        res.append(val)
    return res

def buildmodel(name, data):
    infos = ms.queryRuntimeInfo(name, data)
    points = getCalPoints(infos)
    args = getArgument(points)
    return args
    
#args = buildmodel("file:/home/guolei/scala/KMeans-cluster/target/scala-2.10/simple-project_2.10-1.0.jar", "file:/home/guolei/benchmarkdata/data-Kmeans_200M")

def getThePointFromArguments(args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]

    res = -b/(3*a)

    return int(res)

#args = \
#buildmodel("file:/home/guolei/scala/KMeans-cluster/target/scala-2.10/simple-project_2.10-1.0.jar", \
#"file:/home/guolei/benchmarkdata/data-Kmeans_500M")
#point = getThePointFromArguments(args)
#print point


def getThePointFromPoints(points):
    args = getArgument(points)

    return getThePointFromArguments(args)

#print "the point is " + str(getThePoint(pos))

#l = [1,2,3]
#print str(l)
