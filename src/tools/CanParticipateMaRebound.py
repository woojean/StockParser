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
计算个股明日能否参与5日线反弹
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
  s4 = e1 + e2 + e3 + e4

  print e1,e2,e3,e4
  if 0 == e1*e2*e3*e4:
    print 'End Price Error !'
  else:
    gr5 = s4/(4*e4) - 1
    e5 = (1 + gr5) * e4
    b = (1 + gr5 + 0.01) * e4   
    gr5 = round(gr5,4)
    print 'GR5 = ' + str(gr5*100.0) + '%，E5 = ' + str(e5) + '，B = ' + str(b) + '；'


if __name__ == '__main__':
  (code,parseDay) = getParams()
  print code,parseDay
  compute(code,parseDay)



