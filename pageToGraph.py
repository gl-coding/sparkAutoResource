#!/usr/bin/python

import urllib
import re
import os
import sys
import time
from bs4 import BeautifulSoup

ip = "localhost"

def getLabel(string):
    res = ""
    p = re.compile(r'label=.*')
    result = p.finditer(string)
    for m in result:
        res = m.group()
        break
    res = res.replace(r'label="', "").replace(r'";', "")
    return res

def getIndex(string):
    indexRes = []
    res = ""
    p = re.compile(r'\d* \[label.*')
    result = p.finditer(string)
    for m in result:
        res = m.group()
        indexRes.append(re.match("\d*", res).group())
    return indexRes
        
def getMap(string):
    mapRes = []
    res = ""
    p = re.compile(r'\d*-&gt;\d*;')
    result = p.finditer(string)
    for m in result:
        res = m.group()
        #print res
        res_str = res.replace("-&gt;", " ").replace(";", "")
        edge = "e " + res_str + " 0" + "\n"
        mapRes.append(edge)
    return mapRes

def getJobDag(index, filename):
    #try:
        f = file(filename, "a")
        filecontent = []
        url = "http://" + ip + ":4040/jobs/job/?id=" + str(index)
        #url = "http://10.3.1.82:4040/jobs/job/?id=7"
        graph = "t # " + str(index) + "\n"
        filecontent.append(graph)
        res = ""
        resNum = sys.maxint
        openfile = urllib.urlopen(url)
        html = openfile.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.findAll('div')
        for div in divs:
            divstr = str(div)
            if divstr.find("dot-file") != -1:
                if len(divstr) <= resNum:
                    res = divstr
        #print res
        subres = res.replace("{", "").replace("{", "")
        for unit in re.findall("{[^{]*}", res):
            print unit
            label = getLabel(unit)
            index = getIndex(unit)
            for i in index:
                v = "v " + str(i) + " " + label + "\n"
                filecontent.append(v)
            if unit.find("-&gt;") != -1:
                filecontent.extend(getMap(unit))
            print "======================="
        print filecontent
        mmap = {}
        localIndex = 0
        for line in filecontent:
            if line.startswith("v"):
                i = line.split(" ")[1]
                mmap[i] = localIndex
                localIndex += 1
        for k in mmap:
            if k == mmap[k]:
                del(mmap[k])
        rescontent = []
        for line in filecontent:
            newline = ""
            if not line.startswith("t"):
                for k in mmap:
                    src = " " + str(k) + " "
                    tar = " " + str(mmap[k]) + " "
                    newline = line.replace(src, tar)
            else:
                newline = line
            rescontent.append(newline)
        print rescontent
        f.writelines(rescontent)
        f.close()
    #except Exception, e:
        #print "get DatasetPosition connect error"

#getJobDag(0)

def getJobNum(string):
    res = ""
    p = re.compile("\d+")
    result = p.finditer(string)
    for m in result:
        res = m.group()
        break
    res = res.replace(r'label="', "").replace(r'";', "")
    return res

def getJobs():
    #try:
    filename = "graph.log"
    if os.path.exists(filename):
        os.remove(filename)
    jobs = []
    url = "http://" + ip + ":4040/jobs/"
    while True:
        curMaxJobId = 0
        openfile = urllib.urlopen(url)
        html = openfile.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        #con = str(html)
        lis = soup.findAll('li')
        if str(lis).find("Active Jobs") == -1:
            continue
        if "Completed" not in str(lis):
            curMaxJobId = 0
            print "com"
        else:
            for li in lis:
                listr = str(li)
                if "Completed" in listr:
                    curMaxJobId = int(getJobNum(listr))
        print curMaxJobId
        for curMinJobId in range(0, curMaxJobId+1):
            if curMinJobId in jobs:
                continue
            getJobDag(curMinJobId, filename)
            #print "----------------------"
            jobs.append(curMinJobId)
        print "----------------------"
        time.sleep(3)
    #except Exception, e:
        #print  "get ExefilePosition connect error"

#getJobs()
