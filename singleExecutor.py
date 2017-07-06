#!/usr/bin/python

import urllib
import sys
import os
import re
from bs4 import BeautifulSoup
import math

import time
import mysql as ms
import buildmodel as bm
import getExeInfo as gE
import getMemoryInfo as gM
import advice as advc
import restartSparkApp as rsa
import writeconf as wc
import getCoresPerNode as gcp

times = 0
T = 0.0

#SingleExecutorInitFlag = False
UserConfExecutorStart = True
executorNumConf = 1
executorMemoryConf = 1
executorCoresConf = 1

onlineExpand = True
userMaxCoreConf = False
maxcore = 0

def readStartConf():
    command = "sed -n 1p " + "./config.start"
    args = os.popen(command).read().strip("\n").split(" ")
    times = int(args[0])
    print "try times is " + args[0]
    T = float(args[1])
    print "T per time is " + args[1]
    return args

args = readStartConf()

times = int(args[0])
T = float(args[1])

def readMaxCoreConf():
    configfile = "config.maxcore"
    command = "cat " + configfile
    os.popen(command).read().strip("\n")

if userMaxCoreConf:
    maxcore = readMaxCoreConf()

def writeMemconfig(mem):
    memconfig = "config.mem"
    command = "echo " + str(mem) + " > " + memconfig
    os.system(command)
    
def writeExecutorConfig(corenum):
    coreconfig = "config"
    command = "echo " + str(corenum) + " > " + coreconfig
    os.system(command)

def getMin(arg):
    if arg[-1] == 'n':
        return float(arg.replace(" min", ""))
    elif arg[-1] == 's':
        son = float(arg.replace(" s", ""))
        return son/60.0
    else:
        son = float(arg.replace(" h", ""))
        return son*60.0
    
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

def addExecutor():
    cur = getConf()
    cur += 1
    if maxcore > 0 and cur > maxcore:
        return
    print "add executor num to " + str(cur)
    wc.writeToConfig(cur)

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
    #print recent
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

resultfile = "singleResult"

def writeResult(line):
    f = open(resultfile, "a")
    f.write(line)
    f.close()

#url = sys.argv[1]
url = "http://10.3.1.82:8080"

name = ""
data = ""
core = 0
memory = ""
memUsage = 0.0
runtime = 0
percent = 0.0
conf = 0

SLEEP_INTERVAL = 1

LEN = int(T/(SLEEP_INTERVAL+2)*0.8)

recentInit = []
for val in range(0, LEN):
    recentInit.append(0)

recent = recentInit[:]

index = 0
size = len(recent)

recentMemInit = []
for val in range(0, LEN):
    recentMemInit.append(0)

recentMem = recentMemInit[:]

indexMem = 0
sizeMem = len(recentMem)
flagMemUsage = 1

memoryTotal = 0.0
memoryAvgRatio = 0.0

recordFlag = True
src = 0.0
start = 0.0
end = 0.0

configMem = 1
initMemRatio = 0.0

if UserConfExecutorStart:
    writeExecutorConfig(executorNumConf)
    #rsa.restartMemory(executorMemoryConf)
    rsa.restartInit(executorMemoryConf, executorMemoryConf)

#conf = getConf()
#res = getPercent(recent, conf)
#print res

#exit()

localtimes = 0
globaltimes = times

norunningFlag = True
norunning_starttime = 0
norunning_endtime = 0

program = ""

coresPerNode = 0

while True:
    #try:
        openfile = urllib.urlopen(url)
        html = openfile.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        tds = tables[1].findAll('td')
        tdslen = len(tds)
        #print tdslen

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
                print program
                print runtime
                print coresPerNode
                try:
                    pass
                    #percent = str(getPercent(recent))
                    #conf = str(getConf())
                    #ms.insertRuntimeInfo(name, data, str(core), memory, str(runtime), percent, conf)
                    #num = ms.queryRecordNum(name, data)
                    #print num
                    #if num >= 4:
                        #modelargs = bm.buildmodel(name, data)
                        #thepoint = bm.getThePointFromArguments(modelargs)
                        #modelstr = str(modelargs)
                        #ms.insertmodel(name, data, modelstr, str(thepoint))
                except Exception, e:
                    print "insert error"
                    
            if norunningFlag:
                norunning_starttime = time.time()
                norunningFlag = False
            norunning_endtime = time.time()
            if runtime > 0.0:
                print "((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))"
                string = program + "\t" +  data + " " + str(memory) + "\t" + \
                coresPerNode + "\t"+ str(core) + "\t" + str(runtime) + "\n"
                print string
                writeResult(string)
            noruntimeinterval = norunning_endtime - norunning_starttime
            print noruntimeinterval
            if noruntimeinterval > 60:
                exit()

            print "no running node"
            name = ""
            data = ""
            core = 0
            memory = ""
            memUsage = 0.0
            runtime = 0
            percent = 0.0
            conf = 0
            program = ""
            coresPerNode = 0
        else:
            coresPerNode = gcp.returnCores()
            norunningFlag = True
            norunning_starttime = 0
            norunning_endtime = 0
            if recordFlag == True:
                localtimes = 0
                start = time.time()
                recordFlag = False;

            print "running"
            #name = tds[tdslen-7].getText().strip()
            name = gE.getExePosition()
            try:
                datastr = gE.getDatasetPosition().split(" ")
            except Exception, e:
                print "get datasetPosition return"
                continue
            program = datastr[0]
            datatmp = datastr[1]
            data = datatmp
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
            memUsage = gM.getMemGInfo()/memory
            if memUsage > 1:
                memUsage = 1.0
            indexMem = indexMem % sizeMem
            recentMem[indexMem] = memUsage
            #print recentMem
            indexMem += 1

            memoryTotal = memoryTotal + memUsage
            memoryAvgRatio = memoryTotal/indexMem
            
            ratio = getMemoryOverload(recentMem)
            end = time.time()
            interval = end - start
            print "################################################"
            print "localtimes is " + str(localtimes)
            print "left try times is " + str(times)
            print "time interval is " + str(interval)
            print "cur Executors configure num is " + str(conf)
            print "cur Executors usage is " + str(percent)
            print "Executors usage list is " + str(recent)
            print "cur memory overload ratio is " + str(ratio)
            print "memory usage list is " + str(recentMem)
            print "cur coresPerNode is " + str(coresPerNode)
            print "Online expand is on: " + str(onlineExpand)
            print "------------------------------------------------"
            localtimes += 1
            #if times >=0 and interval > T*(globaltimes-times):
            if times >=0 and interval > T:
                times -= 1
                if ratio < 0.6:
                    corePerExecutor = int(math.floor(1/ratio))
                    rsa.restartCore(corePerExecutor)
                    times = -1
                    recordFlag = True
                    start = 0.0
                    end = 0.0
                    recent = recentInit[:]
                    recentMem = recentMemInit[:]
                elif ratio > 0.8:
                    print "expanding memory offline......"
                    recordFlag = True
                    start = 0.0
                    end = 0.0
                    configMem *= 2
                    #memoryTotal = 0.0
                    recent = recentInit[:]
                    recentMem = recentMemInit[:]
                    rsa.restartMemory(configMem)
                    print "restarting the application......"
                    writeMemconfig(configMem)
                else:
                    print "stop single executor config expand..."
                    initMemRatio = ratio
                    configMem_tmp = int(math.ceil(ratio*configMem))
                    if configMem != configMem_tmp:
                        rsa.restartMemory(configMem)
                        writeMemconfig(configMem)
                    times = -1
                    recordFlag = True
                    start = 0.0
                    end = 0.0
                    recent = recentInit[:]
                    recentMem = recentMemInit[:]
            if times < 0 and interval > T*(0-times) and onlineExpand:
                times -= 1
                print "start expand executor nums online..."
                if percent < 0.95:
                    print "stop expand executor nums online for the core usage is not over load"
                    onlineExpand = False
                elif ratio/initMemRatio < 0.9:
                    print "stop expand executor nums online for the memory usage is getting low"
                    onlineExpand = False
                else:
                    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                    print "current cpu usage is " + str(percent)
                    print "current memory overload ratio is " + str(ratio)
                    addExecutor()
                    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                    print ""
                recordFlag = True
                start = 0.0
                end = 0.0
                recent = recentInit[:]
                recentMem = recentMemInit[:]

            #print memUsage
            #if memUsage > flagMemUsage:
            #    print advc.memoryOverloadWaring
            runtime = getMin(tds[tdslen-1].string.strip())
    #except Exception, e:
     #   print "no master and worker started!!!"
        time.sleep(SLEEP_INTERVAL)
