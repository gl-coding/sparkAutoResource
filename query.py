#!/usr/bin/python

import MySQLdb
import os
import sys
import modelbuild as mb

#dbip = "10.3.1.82"
dbip = "localhost"

def stringToModel(string):
    l = []
    tmp = string.replace("[", "").replace("]", "").replace(" ", "").split(",")
    for val in tmp:
        l.append(float(val))
    return l

def insertRuntimeInfo(name, data, core, coreusage, coreConf, memoryPerNode, \
        memoryusage, runtime, feature, note):
    conn = MySQLdb.connect(host = dbip, port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    sqli = "insert into localruntime values(%s, %s, %s, %s, %s, %s, %s, %s, %s, \
    %s);"
    cur.execute(sqli, (name, data, core, coreusage, coreConf, memoryPerNode, \
        memoryusage, runtime, feature, note))
    cur.close()

    conn.commit()
    conn.close()
    print "insertRuntimeInfo ok"

#insertRuntimeInfo("a", "b", "1", "d", "12", "12.1")

def insertmodel(name, data, arguments, Kvalue, const, memoryPerNode, core):
    conn = MySQLdb.connect(host = dbip, port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    num = cur.execute('select * from localmodel where name = "' + name + '" and data = "' + data + '";')
    if num == 0:
        sqli = "insert into model values(%s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sqli, (name, data, arguments, Kvalue, const, memoryPerNode, core))
    else:
        cur.execute('delete from localmodel where name = "' + name + '" and data = "' + data + '";')
        sqli = "insert into localmodel values(%s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sqli, (name, data, arguments, Kvalue, const, memoryPerNode, core))

    cur.close()

    conn.commit()
    conn.close()
    print "insertmodel ok"
    
#insertmodel("BigDataBench Kmeans", "data", "[-0.034259259259259107, 0.52936507936507571, -2.7506613756613576, 6.0333333333333075]")
    
def querymodel(name):
    conn = MySQLdb.connect(host = dbip, port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    sqlq = "select arguments from localmodel where name = \"" + name + "\";"
    num = cur.execute(sqlq)
    if num == 0:
        return None
    #print cur.fetchone()
    res = cur.fetchone()
    
    string = res[0]
    model = stringToModel(string)
    #print model
    return model

#print querymodel("a")
#print querymodel("BigDataBench Kmeans")

def querymodelNum(name):
    conn = MySQLdb.connect(host = dbip, port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    sqlq = "select arguments from localmodel where name = \"" + name + "\";"
    num = cur.execute(sqlq)
    return num

#print querymodelNum('BigDataBench Kmeans')

def queryRecordNum(name, data):
    conn = MySQLdb.connect(host = dbip, port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    sqlq = 'select * from localruntime where name = "' + name + '" and data = "' + data + '";'
    #print sqlq
    num = cur.execute(sqlq)
    return num 

#print queryRecordNum("a", "b")

def queryRuntimeInfo(name, data):
    conn = MySQLdb.connect(host = dbip, port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    sqlq = 'select memoryPerNode, data, coreConf, runtime from localruntime where \
    note like \'' + name + "%\';"
    #print sqlq
    cur.execute(sqlq)
    #print cur.fetchone()
    res = cur.fetchall()
    reslist = []
    for r in res:
        tmp = []
        tmp.append(name)
        tmp.extend(r)
        reslist.append(tmp)
    return reslist

def listEqual(l1, l2):
    print l1
    print l2
    print "================="
    if len(l1) != len(l2):
        #print "false"
        return False
    for v in range(0, 3):
        print str(l1[v]) + " " + str(l2[v])
        if l1[v] != l2[v]:
            return False
    return True

filename = "data.runtime"

if os.path.exists(filename):
    os.remove(filename)

def writeFile(line):
    f = open(filename, "a")
    f.write(line)
    f.close()
    
trainfile = "data.train"
    
def writeSortedDict(l):
    f = open(trainfile, "w+")
    print "*******"
    print l
    d = {}
    for v in l:
        d[v[0]] = v[1]
    items = d.items()
    items.sort()
    for v in items:
        string = v[0] + "," + v[1] + "\n"
        print string
        f.write(string)
    f.close()

l = []
l.append("Kmeans")
l.append("bfs")
l.append("pr")
l.append("cc")
l.append("lp")
l.append("nbt")
l.append("nb")
l.append("wc")
l.append("sort")

tmp = []

for case in l:
    res = queryRuntimeInfo(case, "")
    reslen = len(res)
    tmplist = []
    for i in range(0, reslen):
        reswidth = len(res[i])
        string = ""
        for v in res[i]:
            string += v + "\t"
        print string
        continue
        resitmp = []
        resitmp.append(res[i][reswidth-2])
        resitmp.append(res[i][-1])
        tmplist.append(resitmp)
        #print tmplist
        if not listEqual(tmp,res[i]):
            print "not equal"
            if len(tmp) != 0:
                print "buildmodel"
                print len(tmplist)
                writeSortedDict(tmplist)
                writeSortedDict(tmplist)
                args = mb.readDatasetFile(trainfile)
                model = mb.getModel(args[0], args[1])
                #print "+++++++++++++++++++++++++++++++++++++++"
                #print tmplist
                #print "+++++++++++++++++++++++++++++++++++++++"
                resitmp = []
                resitmp.append(res[i][reswidth-2])
                resitmp.append(res[i][-1])
                tmplist = []
                tmplist.append(resitmp[:])
        else:
            print "equal"
            if i == reslen-1:
                print "buildmodel"
                print len(tmplist)
                writeSortedDict(tmplist)
                args = mb.readDatasetFile(trainfile)
                model = mb.getModel(args[0], args[1])
                #print "+++++++++++++++++++++++++++++++++++++++"
                #print tmplist
                #print "+++++++++++++++++++++++++++++++++++++++"
        tmp = res[i][:]
        #print tmp
        #print "++++++++++++++++++++++"

        #writeFile(str(r)+"\n")

def getCalPoints(arg):
    a = []
    b = []
    res = []
    for i in range(len(arg)):
        a.append(float(arg[i][0]))
        b.append(float(arg[i][1]))
    res.append(a)
    res.append(b)
    print res

#getCalPoints(res)
