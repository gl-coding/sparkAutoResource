#!/usr/bin/python

import urllib
import re
import os
from bs4 import BeautifulSoup
import classify as csf

def getExePosition():
    try:
        url = "http://localhost:4040/environment/"
        openfile = urllib.urlopen(url)
        html = openfile.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        #con = str(html)
        tables = soup.findAll('table')
        content = str(tables[1])
        command = "echo \"" + content + "\" | grep -o \"<td>spark.jars</td><td>[^<]*</td>\"" 
        line = os.popen(command).read().strip()
        res = line.replace("<td>spark.jars</td>", "").replace("<td>","").replace("</td>", "")
        #print res
        return res
    except Exception, e:
        print  "get ExefilePosition connect error"

#getExePosition()

def getDatasetPosition():
    #try:
    if True:
        url = "http://localhost:4040/environment/"
        openfile = urllib.urlopen(url)
        html = openfile.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        #con = str(html)
        tables = soup.findAll('table')
        content = str(tables[2])
        command = "echo \"" + content + "\" | grep -o \"<td>sun.java.command</td><td>[^<]*</td>\"" 
        line = os.popen(command).read().strip()
        javacommand = line.replace("<td>sun.java.command</td>", "").replace("<td>","").replace("</td>", "")
        #print javacommand
        program = csf.classify(javacommand)
        command = "echo \"" + javacommand + "\" | grep -o \"file:[^ ]*\" | sed -n 1p" 
        line = os.popen(command).read().strip()
        print "+++++++++++++++"
        #print line
        res = ""
        res += program
        res += " " + line
        return res
    #except Exception, e:
        #print "get DatasetPosition connect error"
        
#getDatasetPosition()

#getDatasetPosition()

def getExecutorInfo(appname):
    try:
        url = "http://localhost:4040//api/v1/applications/" + appname + "/allexecutors"
        openfile = urllib.urlopen(url)
        html = openfile.read()
        print html
    except Exception, e:
        print "get DatasetPosition connect error"

#getExecutorInfo("app-20170221160622-0010")
