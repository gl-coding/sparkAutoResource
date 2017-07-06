#!/usr/bin/python

import web
import mysql as ms

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        info = web.input()
        jsonStr = info
        print jsonStr
        exit()
        name = d['name'] 
        data = d['data']    
        core = d['core']    
        percent = d['percent'] 
        conf = d['conf']    
        memory = d['memory']
        ratio = d['ratio']   
        runtime = d['runtime'] 
        feature = d['feature'] 
        note = d['note']
        try:
            ms.insertRuntimeInfo(name, data, core, coreusage, coreConf, \
                    memoryPerNode, memoryusage, runtime, feature, note)
        except Exception, e:
            print "insert error"

        return "ok"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
