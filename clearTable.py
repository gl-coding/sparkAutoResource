#!/usr/bin/python

import MySQLdb

def deleteTable(table):
    conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd='123456', db = 'program_feature',)
    cur = conn.cursor()
    sqld = "delete from " + table + ";"
    cur.execute(sqld)
    cur.close()

    conn.commit()
    conn.close()
    print "delete " + table + " ok"

deleteTable("baseInfo")

deleteTable("model")
