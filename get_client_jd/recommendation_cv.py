#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import pycurl
import time
import StringIO

url = 'http://192.168.8.204:6688/?handle=recommendation&m=jd&jd_id=17684742'
url2 = 'http://192.168.8.204:6688/?handle=recommendation&m=jdcv_matchscore&jd_id=1200535&cv_id=12085919'
b = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(pycurl.URL,url)
c.setopt(pycurl.HTTPHEADER,["Accept:"])
c.setopt(pycurl.WRITEFUNCTION,b.write)
c.setopt(pycurl.FOLLOWLOCATION,1)
c.setopt(pycurl.MAXREDIRS,5)

c.perform()
print b.getvalue()
b.close()
c.close()

