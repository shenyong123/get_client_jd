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

def process_client_competitor_id(results):
    client_competitor_id = []
    client = []
    competitor = []
    # init the corp_self
    client.append(results[0][2])
    if results[0][5].strip():
        tmp_id = results[0][5].split(',')
        for id in tmp_id:
            client.append(id)

    n = len(results)
    for i in range(1, n):
        if results[i][0] == results[i - 1][0]:
            competitor.append(results[i][2])
            if results[i][5].strip():
                tmp_id = results[i][5].split(',')
                for id in tmp_id:
                    competitor.append(int(id))
        else:
            client_competitor_id.append((client, competitor))
            client = [results[i][2]]
            if results[i][5].strip():
                tmp_id = results[i][5].split(',')
                for id in tmp_id:
                    client.append(int(id))
            competitor = []
    return client_competitor_id

#105
def getClientCompitorID(host,port=3307,user=None,passwd=None):
    """get the client and his competitors' corporation_id"""
    conn = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd)
    cursor = conn.cursor()
    sql1 = "select * from data_service.account_bind "
    sql2 = "select account_bind.corporation_id,account_bind.corporation_name,resume_list.icdc_id from account_bind,resume_list where account_bind.corporation_id=resume_list.corporation_id  and account_bind.bind_or_benchmark=0 \G;"
    # sql2 = "select * from data_service.account_bind where bind_or_benchmark=0 limit 10\G"
    cursor.execute(sql1)
    # all data in account_bind
    results = cursor.fetchall()
    client_competitor_ids = process_client_competitor_id(results)
    conn.close()
    return client_competitor_ids



#134
def getClientCompetitor_jd_id(client_competitor_ids,host,port=3307,user=None,passwd=None):
    """get the jd_id and corporation_id of client and competitor
       the result : client_competitor_info is like{"client123243":{'client':[[r0,r1],...],'competitor':[[r0,r1],...]}}
       r0 is jd_id ,r1 is corporation_id;
    """
    conn2 = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd)
    cursor = conn2.cursor()
    cursor.execute("set names utf8")
    conn2.commit()
    client_competitor_info = dict()
    for cc_id in client_competitor_ids:
        client_jd_id = []
        competitor_jd_id = []
        for c_id in cc_id[0]:
            for i in range(0,16,2):         # i is the number of the position_ in databases;
                sql2 = get_sql(str(i),c_id)      #c_id is the client corporation_id
                cursor.execute(sql2)
                results1 = cursor.fetchall()
                # for info in s_info:
                for r in results1:
                    print r[2] + " " + r[3]
                    client_jd_id.append([r[0],r[1]])

        if cc_id[1]:
            for c_id in cc_id[1]:
                for i in range(0,16,2):
                    sql3 = get_sql(str(i),c_id)
                    cursor.execute(sql3)
                    results2 = cursor.fetchall()
                    for r in results2:
                        print r[2] + " " + r[3]
                        competitor_jd_id.append([r[0],r[1]])

        client_competitor_info['client'+str(cc_id[0][0])] = {'client':client_jd_id,'comptitor':competitor_jd_id}
    conn2.close()
    return client_competitor_info


host1 = '192.168.8.105'
host2 = '192.168.8.134'
port = 3307
user ="kdd"
passwd = 'GeYFL4EU,tcOtP$W'
client_competitor_ids = getClientCompitorID(host1,port,user,passwd)
for info in client_competitor_ids:
    print info

client_competitor_info = getClientCompetitor_jd_id(client_competitor_ids,host2,port,user,passwd)
for info in client_competitor_info:
    print info
    print client_competitor_info[info]