#!/usr/bin/python

import os

conf_pos = "/home/guolei/sparkInfo/config"

def writeToConfig(conf):
    command = "echo " + str(conf) + " > " + conf_pos
    os.system(command)
    
def readConfig():
    command = "cat " + conf_pos
    print os.popen(command).read().strip("\n")

writeToConfig(10)
readConfig()
