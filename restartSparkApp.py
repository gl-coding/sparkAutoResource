#!/usr/bin/python

import os

def killSpark():
    command = "jps"
    res = os.popen(command).read().strip('\n').split('\n')
    if len(res) > 1:
        for val in range(0, len(res)):
            print res[val]
            args = res[val].split(" ")
            pid = args[0]
            name = args[1]
            com = "kill -9 " + pid
            os.system(com)

def startSpark():
    command = "./restart"
    os.system(command)

#killSpark()

def killSparkApp():
    command = "jps"
    res = os.popen(command).read().strip('\n').split('\n')
    for val in range(0, len(res)):
        print res[val]
        args = res[val].split(" ")
        pid = args[0]
        name = args[1]
        if name == "Master" or name == "Worker" or name == "Jps":
            continue
        else:
            com = "kill -9 " + pid
            os.system(com)
    command = "jps"
    res = os.popen(command).read().strip('\n').split('\n')
    if len(res) == 3:
        print "kill successfully"
    else:
        print "kill fail......"
        
#killSparkApp()
#exit()

def restartApp(directory, exefile):
    command = "cd " + directory + ";nohup ./" + exefile + " &>sparkrun.log&"
    os.system(command)

def readExefileInfo(config):
    command = "sed -n 1p " + config
    args = os.popen(command).read().strip("\n").split(" ")
    #directory = args[0]
    #exefile = args[1]
    #print directory
    #print exefile
    return args

def writeMemconfig(mem):
    command = "./changeMemory " + str(mem)
    os.system(command)

def writeExecutorCoreconfig(core):
    command = "./changeCore " + str(core)
    os.system(command)

def restartMemory(memory):
    killSparkApp()
    writeMemconfig(memory)
    args = readExefileInfo("config.run")
    restartApp(args[0], args[1])

def restartCore(core):
    killSparkApp()
    writeExecutorCoreconfig(core)
    args = readExefileInfo("config.run")
    restartApp(args[0], args[1])
    
def restartInit(memory, core):
    killSparkApp()
    writeMemconfig(memory)
    writeExecutorCoreconfig(core)
    args = readExefileInfo("config.run")
    restartApp(args[0], args[1])

#args = readExefileInfo("./config.run")
#restartApp(args[0], args[1])

#restart(4)
