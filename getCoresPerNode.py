#!/usr/bin/python

import os

def returnCores():
    command = "./getCoresPerNode.sh"
    res = os.popen(command).read().strip("\n")
    #print res
    return res
