#!/usr/bin/python

import mysql as ms
import buildmodel as bm
import writeconf  as wc

def useModel(name):
    num = ms.querymodelNum()
    if num = 0:
        pass
    else:
        model = ms.querymodel(name)
        point = bm.getCalPoints()
        wc.writeToConfig(point)

useModel("BigdataBench Kmeans")

