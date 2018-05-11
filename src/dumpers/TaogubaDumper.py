#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-08
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

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser


def parseArticleList(path):
  res = open(path,'r').read()
  l = eval(res)
  return l

def dumpReport(articleList):
  s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
  s += '''
<style>
font-size:0.8em;

td{
  font-size:0.8em;
  text-align:center;
  padding:5px;
  border-bottom: thin dotted #ccc;
}

tr:hover{
  background-color:yellow;
  cursor:pointer;
}
</style>
  '''
  s += '</head><body>'

  s += '<table>'
  s += '<tr><td>序号</td><td>标题</td><td>回复数</td></tr>'
  no = 1
  for article in articleList:
    tr = '<tr>'
    tr += '<td>'
    tr += str(no)
    tr += '</td>'
    tr += '<td>'
    tr += '<a href=' + HOST + article['href']+ ' target="_blank">' + str(article['title'])+'</a>'
    tr += '</td>'
    tr +='<td>'
    tr += str(article['response'])
    tr +='</td>'
    tr +='</tr>'
    s += tr
    no += 1

  path = Tools.getReportDirPath()+'/'+'Taoguba-Hot.html'
  open(path,'w').write(s)
  os.system('open '+path)


HOST = 'https://www.taoguba.com.cn/'

if __name__ == '__main__':
  articleList = []
  taogubaPath = Tools.getTaogubaDataPath()
  for root,dirs,files in os.walk(taogubaPath):
    for f in files:
      try:
        path = root + '/' + f
        l = parseArticleList(path)
        articleList = articleList + l
      except Exception, e:
        pass
        #print repr(e)
  dumpReport(articleList)







