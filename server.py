#!/usr/bin/env python
import web
import json
import mysql as ms

urls = (
    '/', 'index'
)

class index:
    def POST(self):
        # How to obtain the name key and then print the value?
        d = json.loads(web.data())
        print d
        name = d['name'] 
        data = d['data']    
        core = d['core']    
        coreusage = d['percent'] 
        coreConf = d['conf']    
        memoryPerNode = d['memory']
        memoryusage = d['ratio']   
        runtime = d['runtime'] 
        feature = d['feature'] 
        note = d['note']
        
        #try:
        if True:
            ms.insertRuntimeInfo(name, data, core, coreusage, coreConf, \
                    memoryPerNode, memoryusage, runtime, feature, note)
        #except Exception, e:
            #print "insert error"
        return "Ok"

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
