#coding:utf-8
#!/usr/bin/env python
import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser


# ------------------------------------------------------------------------

def dumpReport(ret):
  tPath = Tools.getRootPath()+'/src/tools/T_EndPriceComparators.html'
  for code,data in ret.items():
    s = '['
    detail = ''
    t = open(tPath,'r').read()
    for item in data:
      s += str(item[1]) + ','
      detail +=item[0] + ' : ' + str(item[1]) + '<br/>'
    s = s[:-2]
    s +='];'
    t = t.replace('$DATA$',s)

    name = Tools.getNameById(code)
    t = t.replace('$CODE$',code +' '+name)
    t = t.replace('$DETAILS$',detail)
    path = Tools.getReportDirPath()+'/EndPriceCompareReport-'+code+'.html'
    open(path,'w').write(t)
    os.system('open '+path)



def getRes(code,parseDay):
  parser = BaseParser.BaseParser(parseDay)
  priceFile = Tools.getPriceDirPath()+'/'+str(code)
  res = open(priceFile,'r').read()
  return res



def compare(compareTo,compareList):
  ret = {}
  parseDay = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
  parser = BaseParser.BaseParser(parseDay)
  dayList = parser.getPastTradingDayList(parseDay,compareDays)
  for code in compareList:
    for day in dayList:
      res1 = getRes(compareTo,parseDay)
      endPrice1 = parser.getEndPriceOfDay(res1,day)
      res2 = getRes(code,parseDay)
      endPrice2 = parser.getEndPriceOfDay(res2,day)
      rate = round(endPrice2/endPrice1,5)*100.0
      if not ret.has_key(code):
        ret[code] = [(day,rate)]
      else:
      	ret[code].append((day,rate))
  return ret



# ------------------------------------------------------------------------
compareDays = 60
compareTo = '000001'
compareList = [
  '002123',
  '002370',
  '002668',
  '600638',
  '002686',
  '600532',
]


if __name__ == '__main__':
  ret = compare(compareTo,compareList)
  dumpReport(ret)
  



