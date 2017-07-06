#!/usr/bin/python

import MySQLdb

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
    sqlq = 'select core, runtime from runtime where name = "' + name + '" and data = "' + data + '";'
    cur.execute(sqlq)
    #print cur.fetchone()
    res = cur.fetchall()
    return res

#res = queryRuntimeInfo("a", "b")
#print res

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
