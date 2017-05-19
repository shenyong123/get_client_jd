#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

def any2utf8(text, errors='strict', encoding='utf8'):
    """Convert a string (unicode or bytestring in `encoding`), to bytestring in utf8."""
    if isinstance(text, unicode):
        return text.encode('utf8')
    # do bytestring -> unicode -> utf8 full circle, to ensure valid utf8
    return unicode(text, encoding, errors=errors).encode('utf8')

def get_sql(ku_id,corporation_id):
    if ku_id and corporation_id:
        sql = "select id,corporation_id,corporation_name,name from position_" + str(ku_id) + ".positions where corporation_id=" + str(corporation_id) +" and status=0"
        return sql
    else:
        print"parm is not enough!"

def get_self_competitor_id(result):
    self_competitor_id = []
    corp_self = []
    competitor = []
    # init the corp_self
    corp_self.append(results[0][2])
    if results[0][5].strip():
        tmp_id = results[0][5].split(',')
        for id in tmp_id:
            corp_self.append(id)

    n = len(results)
    for i in range(1, n):
        if results[i][0] == results[i - 1][0]:
            competitor.append(results[i][2])
            if results[i][5].strip():
                tmp_id = results[i][5].split(',')
                for id in tmp_id:
                    competitor.append(int(id))
        else:
            self_competitor_id.append((corp_self, competitor))
            corp_self = [results[i][2]]
            if results[i][5].strip():
                tmp_id = results[i][5].split(',')
                for id in tmp_id:
                    corp_self.append(int(id))
            competitor = []
    return self_competitor_id

#105
conn = MySQLdb.connect(host='192.168.8.105',port=3307,user='kdd',passwd='GeYFL4EU,tcOtP$W')
cursor = conn.cursor()
sql1 = "select * from data_service.account_bind "
# sql2 = "select * from data_service.account_bind where bind_or_benchmark=0 limit 10\G"
cursor.execute(sql1)
# all data in account_bind
results = cursor.fetchall()

self_competitor_ids = get_self_competitor_id(results)

conn.close()

for info in self_competitor_ids:
    print info

#134
conn2 = MySQLdb.connect(host='192.168.8.134',port=3307,user='kdd',passwd='GeYFL4EU,tcOtP$W')
cursor = conn2.cursor()
for i in range(0,16,2):
    sql2 = get_sql(str(i), 1228443)  # name is position name
    print sql2
    cursor.execute("set names utf8")
    conn2.commit()
    cursor.execute(sql2)
    infos = cursor.fetchall()
    for info in infos:
        print info

conn2.close()

