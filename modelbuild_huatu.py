#!/usr/bin/python

import matplotlib.pyplot as plt
from sklearn import cross_validation
import numpy as np
import scipy as sp
import urllib

def error(f, x, y):
    return sp.sum((f(x)-y)**2)

def getFx(datax, datay, degree):
    fp1= sp.polyfit(datax, datay, degree)
    #print fp1
    #aa = polyval(fp1, 5)
    #print aa
    fStraight = sp.poly1d(fp1)
    return fStraight
    
def huatu(index, datax, datay, degree, labelx, labely):
    plt.subplot(index)
    plt.scatter(datax, datay)
    plt.autoscale(tight=True)
    plt.grid()
    
    fp1= sp.polyfit(datax, datay, degree)
    print fp1
    #aa = polyval(fp1, 5)
    #print aa
    fStraight = sp.poly1d(fp1)
    print "Error of Curve3 line:",error(fStraight,datax,datay)
    #draw fitting straight line
    fx = sp.linspace(0,datax[-1], 10) # generate X-values for plotting
    plt.plot(fx, fStraight(fx), linewidth=4)
    #plt.legend(["d=%i" % fStraight.order], loc="upper left")
    plt.xlabel(labelx)
    plt.ylabel(labely)
    
def getPartOfList(listarg, num, preflag):
    res = []
    if preflag:
        res = listarg[0:num]
    else:
        res = listarg[num-1:len(listarg)]
    return res

def getPreModel(x, y, maxdegree):
    print "build premodel"
    if len(x) < 3:
        return ""
    dictory = {}
    for degree in range(1, maxdegree):
        for val in range(1, 5):
            print val
            ratio = val/10.0
            x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=ratio, random_state=0)
            if len(x_train) < 3:
                continue
            fx = getFx(x_train, y_train, degree)
            e = error(fx, x_test, y_test)/len(x_test)
            tupletmp = (degree, fx)
            dictory[e] = tupletmp
    items = dictory.items()
    print items
    items.sort()
    print items[0]
    return items[0]

def getPostModel(x, y):
    dictory = {}
    for val in range(1, 5):
        ratio = val/10.0
        print "testsize :" + str(ratio)
        x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=ratio, random_state=0)
        if len(x_train) < 1:
            continue
        fx = getFx(x_train, y_train, 0)
        e = error(fx, x_test, y_test)/len(x_test)
        print "error avg :" + str(e)
        dictory[e] = fx
    items = dictory.items()
    items.sort()
    print items[0]
    return items[0]

def getStraightLine(x, y):
    fx = getFx(x, y, 0)
    return fx[0]

def getInnerPoints(x, y, value):
    resx = []
    resy = []
    for val in range(0, len(x)):
        if y[val] < value*1.5:
            resx.append(x[val])
            resy.append(y[val])
    return resx[0]


#l = [1, 2, 3]
#print getPartOfList(l, 2, True)
#print getPartOfList(l, 2, False)
    
def getModel(X, Y):
    datasetLen = len(X)
    print "dataset length is " + str(datasetLen)
    if datasetLen < 3:
        return "data too less"

    model = {}
    kset = set([])

    for val in range(datasetLen, 3, -1):
        print val
        postX = getPartOfList(X, val, False)
        postY = getPartOfList(Y, val, False)
        print postX
        print postY
        value = getStraightLine(postX, postY)
        print "post line avg: " + str(value)
        kvalue = getInnerPoints(X, Y, value)
        print "kvalue is " + str(kvalue)
        if kvalue in kset:
            pass
        else:
            kset.add(kvalue)

        postX = getPartOfList(X, kvalue, False)
        postY = getPartOfList(Y, kvalue, False)

        postmodel = getPostModel(postX, postY)
        error2 = postmodel[0]
        model2 = postmodel[1]

        preX = getPartOfList(X, kvalue, True)
        preY = getPartOfList(Y, kvalue, True)
        premodel = getPreModel(preX, preY, int(kvalue))
        if premodel == "":
            error1 = 0
            model1 = ""
        else:
            error1 = premodel[0]
            model1 = premodel[1]

        error = (error1 + error2)/2
        singlemodel = (model1, kvalue, model2)
        model[error] = singlemodel
    if len(model) < 1:
        return "model build error"
    items = model.items()
    items.sort()
    print "result is:++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print items[0]
    return items[0]
    
def readDatasetFile(datafile):
    res = []
    cols=2
    begin,end = 0,2
    categorycol=1
    raw_data = urllib.urlopen(datafile)
    dataset = np.loadtxt(raw_data, delimiter=",", usecols=range(cols))
    x = dataset[:,0:end]
    y = dataset[:,categorycol]

    X = x[:,0]
    Y = x[:,1]

    print X
    print Y
    res.append(X)
    res.append(Y)
    return res

def getPreModelArguments(model):
    res = []
    fx = model[1][0][1]
    for val in fx:
        res.append(val)
    return res
    
def getKvalue(model):
    return model[1][1]
    
def getpostModelArgments(model):
    res = []
    fx = model[1][2]
    for val in fx:
        res.append(val)
    return res

def stringToModel(string):
    l = []
    tmp = string.replace("[", "").replace("]", "").replace(" ", "").split(",")
    for val in tmp:
        l.append(float(val))
    return l

def getYFromX(args, x):
    res = 0
    reverse = args[::-1]
    for val in range(0, len(reverse)):
        tmp = reverse[val]
        for v in range(0, val):
            tmp *= x
        res += tmp
    return res

def getModelValue(model, x):
    if len(model[1]) == 3:
        k = model[1][1]
        pre = model[1][0]
        premodel = pre[1]
        postmodel = model[1][2]
        if x <= k:
            return premodel(x)
        else:
            return postmodel(x)
    else:
        print "stright line"

def printModelInfo(model):
    error = model[0]
    print error
    pre = model[1][0]
    premodel = pre[1](1)
    print premodel
    k = model[1][1]
    print k
    post = model[1][2]
    print post

args = readDatasetFile("train.file")
#args = readDatasetFile("data.train")
model = getModel(args[0], args[1])
print "*************************************"

print getModelValue(model, 1)
print getModelValue(model, 6)
