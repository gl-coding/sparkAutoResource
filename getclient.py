#!/usr/bin/python
import urllib2

url = "http://10.3.1.82:6666/?array=aaa"

res_data = urllib2.urlopen(url)
res = res_data.read()
print res
