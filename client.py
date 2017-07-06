#!/usr/bin/python

import os
import json

def genJson(name, data, core, percent, conf, memory, ratio, runtime, feature, note):
    d = {}
    d['name']    = name
    d['data']    = data
    d["core"]    = core
    d['percent'] = percent
    d['conf']    = conf
    d['memory']  = memory
    d['ratio']   = ratio
    d['runtime'] = runtime
    d['feature'] = feature 
    d['note']    = note
    res = json.dumps(d)
    return res

#jsonStr = genJson("a", "b")

def genDict(jsonStr):
    json_to_python = json.loads(jsonStr)
    print json_to_python
    print type(json_to_python)

#d = genDict(jsonStr)

def sendData(data):
    command = '''curl -H "Content-Type: application/json" -X POST -d ''' + "'" \
        + str(data) + "'" + ''' http://10.3.1.82:6666/'''
    print command
    res = os.popen(command).read().strip("\n")
    #print res;

#sendData("first")

def writeData(name, data, core, percent, conf, memory, ratio, runtime, feature, note):
    jsonStr = genJson(name, data, core, percent, conf, memory, ratio, runtime, feature, note)
    print jsonStr
    sendData(jsonStr)
    
#writeData("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")
