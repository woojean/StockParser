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

'''
用“明日涨停价”算最大MA5
'''


def getParams():
  code = False if (len(sys.argv) <= 1) else sys.argv[1]
  parseDay = time.strftime('%Y-%m-%d',time.localtime(time.time())) if (len(sys.argv) <= 2) else sys.argv[2]
  return (code,parseDay)


def getRes(code,parseDay):
  parser = BaseParser.BaseParser(parseDay)
  priceFile = Tools.getPriceDirPath()+'/'+str(code)
  res = open(priceFile,'r').read()
  return res


def compute(code,parseDay):
  res = getRes(code,parseDay)
  parser = BaseParser.BaseParser(parseDay)
  dayList = parser.getPastTradingDayList(parseDay,4)
  print dayList
  e1 = parser.getEndPriceOfDay(res,dayList[0])
  e2 = parser.getEndPriceOfDay(res,dayList[1])
  e3 = parser.getEndPriceOfDay(res,dayList[2])
  e4 = parser.getEndPriceOfDay(res,dayList[3])
  e5 = e4 * 1.1
  
  print e1,e2,e3,e4,e5
  if 0 == e1*e2*e3*e4:
    print 'End Price Error !'
  else:
    ma3 = (e3+e4+e5)/3.0
    ma5 = (e1+e2+e3+e4+e5)/5.0
    print 'MA3 = ' + str(ma3)+'，MA5 = ' + str(ma5)


if __name__ == '__main__':
  (code,parseDay) = getParams()
  print code,parseDay
  compute(code,parseDay)



