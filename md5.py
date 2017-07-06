#!/usr/bin/python

import hashlib

def toMD5String(string):
    m2 = hashlib.md5()
    m2.update(string)
    return m2.hexdigest()


#print toMD5String("a")
