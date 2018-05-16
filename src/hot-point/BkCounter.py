#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-04
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new
from operator import itemgetter 

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools


def countBkShowTimes():
  d = {}
  path = Tools.getRootPath()+'/db/db-hot-bk/'
  for root,dirs,files in os.walk(path):
    for f in files:
      try:
         path = root + '/' + f
         s = open(path,'r').read()
         arr = s.split(',')
         for bk in arr:
           if d.has_key(bk):
             d[bk] +=1
           else:
           	 d[bk] = 1
      except Exception, e:
        pass
        #print repr(e)
  return d


def dumpBkReport(allBk,bkShowTimes):
  pass
  s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
  s += '''
<style>
font-size:0.8em;

table {
  width:100%;
}

td{
  font-size:0.8em;
  text-align:center;
  padding:5px;
  border-bottom: thin dashed #ccc;
}

.table_header{
  font-weight:bold;
  font-size:1.2em;
}

</style>
  '''
  s += '</head><body>'
  s += '<table width="100%" cellspacing="0" cellpadding="0">'
  s += '<tr class="table_header">'
  s += '<td>序号</td>'
  s += '<td>板块名称</td>'
  s += '<td>出现次数</td>'
  s += '</tr>'

  bkList = []
  for bkCode,bkInfo in allBk.items():
    times = 0
    if bkShowTimes.has_key(bkInfo[1]):
      times = bkShowTimes[bkInfo[1]]
    bk = (bkInfo,times)
    bkList.append(bk)

  # 排序
  bkList = sorted(bkList,key=lambda i: (-i[1]))

  i = 1
  for bk in bkList:
    tr = '<tr>'
    tr += '<td>'+str(i) +'</td>'
    i += 1
    tr += '<td>'+ str(bk[0][1]) +'</td>'
    tr += '<td>'+ str(bk[1]) +'</td>'
    s += tr
  s += '</table>'

  parseTime = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
  path = Tools.getReportDirPath()+'/BK-Count.html'
  open(path,'w').write(s)
  os.system('open '+path)


if __name__ == '__main__':
  path = Tools.getRootPath()+'/data/hot-point-sniffer/bk-dict'
  allBk = eval(open(path,'r').read())
  
  bkShowTimes = countBkShowTimes()
  dumpBkReport(allBk,bkShowTimes)


