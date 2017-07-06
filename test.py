#!/usr/bin/python
import mysql as ms

#ms.insert("a", "a", "a", "a")

s = "<a>"

a =  s.replace("\<.+\>", "")
print a
