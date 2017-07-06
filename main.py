#!/usr/bin/python

import urllib
import sys
import os
import re
from bs4 import BeautifulSoup

import time
import mysql as ms
#import buildmodel as bm
import getExeInfo as gE
import getMemoryInfo as gM
import advice as advc
import md5 as md
import pageToGraph as pg
import client as cl

def getLinuxPath(arg):
    path = arg.replace("file:", "")

def getAmount(arg):
    resAmount = 0.0
    path = arg.replace("file:", "")
    if not os.path.exists(path):
        return -1
    command = "du -h " + path + " | tail -1 | awk -F' ' '{print $1}'"
    res = os.popen(command).read().strip("\n")
    print res
    if res.endswith("K"):
       res = res.replace("K", "")
       resAmount = float(res)/1024/1024
    elif res.endswith("M"):
       res = res.replace("M", "")
       resAmount = float(res)/1024
    else:
       res = res.replace("G", "")
       resAmount = float(res)
    return resAmount

def getMin(arg):
    try:
        if arg[-1] == 'n':
            return float(arg.replace(" min", ""))
        elif arg[-1] == 's':
            son = float(arg.replace(" s", ""))
            return son/60.0
        else:
            son = float(arg.replace(" h", ""))
            return son*60.0
    except Exception, e:
        return 0
    
def getMemoryG(arg):
    if arg.endswith("MB"):
        return float(arg.replace(" MB", ""))/1024
    else:
        return float(arg.replace(" GB", ""))

def getConf():
    config_pos = "./config"
    command = "cat " + config_pos
    res = os.popen(command).read().strip()
    #print res
    return int(res)

def getMemoryOverload(recentMem):
    length = len(recentMem)
    ratio = 0.0
    memorysum = 0.0
    for val in range(0, length):
        memorysum += recentMem[val]
    #print length
    ratio = float(memorysum)/length
    return ratio

def getPercent(recent):
    print recent
    conf = getConf()
    #print conf
    count = 0.0
    for val in recent:
        count += val;
    percent = count/float((len(recent)*conf))
    #print count
    #print float(len(recent)*conf)
    #print percent
    return percent

#getConf()
#exit()
        
def getOnePage(url, filename):
    response = urllib.urlopen(url).read()
    soup = BeautifulSoup(response)
    alltext = soup.get_text().strip('\n')
    #print alltext
    single = filename
    with open(single, "w") as f:
        f.write(alltext.encode('utf-8'))
    f.close()

def fileToList(filename):
    res = []
    for line in open(filename, "r"):
        res.append(line)
    return res

def getIP():
    command = "ifconfig | grep -o '10.3.1.[^ ]*'"
    ip = os.popen(command).read().strip("\n")
    return ip

#url = sys.argv[1] 
url = "http://localhost:8080"

name = ""
data = ""
core = 0
memory = ""
memUsage = 0.0
runtime = 0
percent = 0.0
conf = 0
note = ""

recentInit = []
for val in range(0, 10):
    recentInit.append(0)

recent = recentInit[:]

index = 0
size = len(recent)

recentMemInit = []
for val in range(0, 10):
    recentMemInit.append(0)

recentMem = recentMemInit[:]

indexMem = 0
sizeMem = len(recentMem)
flagMemUsage = 1

jobsurl = "http://localhost:4040/jobs/"
graphfile = "graph.main"
if os.path.exists(graphfile):
   os.remove(graphfile)
jobs = []
curMaxJobId = 0

coresPerNode = 0

#conf = getConf()
#res = getPercent(recent, conf)
#print res

#exit()

while True:
    #try:
        try:
            openfile = urllib.urlopen(url)
        except Exception, e:
            print "Spark Master and Worker not started"
            time.sleep(2)
            continue
        html = openfile.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        tds = tables[1].findAll('td')
        tdslen = len(tds)
        print tdslen

        if tdslen == 0:
            if name != "":
                print "insert"
                print name
                print data
                print core
                print memory
                print memUsage
                print runtime
                print percent
                print conf
                print ratio
                print note
                #try:
                if True:
                    percent = str(getPercent(recent))
                    conf = str(getConf())
                    seqs = str(fileToList(graphfile)).replace("'", "@")
                    print seqs
                    length = min(200, len(seqs))
                    feature = seqs[0:length]
                    cl.writeData(name, data, str(core), str(percent), str(conf), str(memory), str(ratio), str(runtime),
                            feature, note)
                #except Exception, e:
                    #print "insert error"
            print "no spark app running"
            name = ""
            data = ""
            core = 0
            memory = ""
            memUsage = 0.0
            runtime = 0
            percent = 0.0
            conf = 0
            ratio = 0.0
            note = ""
            jobs = []
            recent = recentInit[:]
            recentMem = recentMemInit[:]
            if os.path.exists(graphfile):
                os.remove(graphfile)
        else:
            print "running"
            #name = tds[tdslen-7].getText().strip()
            try:
                position = gE.getExePosition()
                name = md.toMD5String(position)
            except Exception, e:
                print "get ExePosition return"
                continue
            curdate = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            ip = getIP()
            try:
                datastr = gE.getDatasetPosition().split(" ")
            except Exception, e:
                print "get datasetPosition return"
                continue
            program = datastr[0]
            datatmp = datastr[1]
            note = program + ";" + ip + ";" + str(curdate) + ";"
            note += position + ";" + datatmp + ";"
            print note
            data = getAmount(datatmp)
            core = tds[tdslen-6].string.strip()
            
            index = index % size
            recent[index] = int(core)
            index += 1

            percent = getPercent(recent)
            conf = getConf()
            #print recent
            #print conf
            memory = getMemoryG(tds[tdslen-5].string.strip())
            #print "error"
            print memory
            memUsage = gM.getMemGInfo()/memory
            indexMem = indexMem % sizeMem
            recentMem[indexMem] = memUsage
            indexMem += 1
            ratio = getMemoryOverload(recentMem)
            print "ratio " + str(ratio)
            #print memUsage
            #if memUsage > flagMemUsage:
            #    print advc.memoryOverloadWaring
            runtime = getMin(tds[tdslen-1].string.strip())


            curMaxJobId = 0
            try:
                openfile = urllib.urlopen(jobsurl)
            except Exception, e:
                print "get jobs Graph return"
                continue
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
                        curMaxJobId = int(pg.getJobNum(listr))
            print curMaxJobId
            for curMinJobId in range(0, curMaxJobId+1):
                if curMinJobId in jobs:
                    continue
                pg.getJobDag(curMinJobId, graphfile)
                #print "----------------------"
                jobs.append(curMinJobId)
                print "----------------------"
    #except Exception, e:
        #print "no master and worker started!!!"
        time.sleep(2)
