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


def computeMaxMa(code,parseDay):
  res = getRes(code,parseDay)
  parser = BaseParser.BaseParser(parseDay)
  dayList = parser.getPastTradingDayList(parseDay,4)
  e1 = parser.getEndPriceOfDay(res,dayList[0])
  e2 = parser.getEndPriceOfDay(res,dayList[1])
  e3 = parser.getEndPriceOfDay(res,dayList[2])
  e4 = parser.getEndPriceOfDay(res,dayList[3])
  e5 = e4 * 1.1
  
  if 0 == e1*e2*e3*e4:
    print 'End Price Error !'
  else:
    ma5 = round((e1+e2+e3+e4+e5)/5.0,4)
    ma3 = round((e3+e4+e5)/3.0,4)

    gr5 = round((ma5-e4)/e4,5)
    gr3 = round((ma3-e4)/e4,5)
    print '涨停5日线：MA5 = ' + str(ma5)+ '，GR5 = ' + str(gr5*100.0) + '%'
    print '涨停3日线：MA3 = ' + str(ma3)+ '，GR5 = ' + str(gr3*100.0) + '%'



def computeReboundMa(code,parseDay):
  res = getRes(code,parseDay)
  parser = BaseParser.BaseParser(parseDay)
  dayList = parser.getPastTradingDayList(parseDay,4)
  e1 = parser.getEndPriceOfDay(res,dayList[0])
  e2 = parser.getEndPriceOfDay(res,dayList[1])
  e3 = parser.getEndPriceOfDay(res,dayList[2])
  e4 = parser.getEndPriceOfDay(res,dayList[3])
  s4 = e1 + e2 + e3 + e4

  if 0 == e1*e2*e3*e4:
    print 'End Price Error !'
  else:
    gr5 = s4/(4*e4) - 1
    e5 = (1 + gr5) * e4
    # b = (1 + gr5 + 0.000) * e4   
    gr5 = round(gr5,4)
    print '回踩5日线：MA5 = ' + str(e5) + '，GR5 = ' + str(gr5*100.0) + '%'

    gr3 = (e3+e4)/(2*e4) - 1
    e = (1 + gr3) * e4
    # b = (1 + gr3 + 0.000) * e4   
    gr3 = round(gr3,4)
    print '回踩3日线：MA3 = ' + str(e) + '，GR3 = ' + str(gr3*100.0) + '%' 

if __name__ == '__main__':
  (code,parseDay) = getParams()
  print code,parseDay
  computeReboundMa(code,parseDay)
  computeMaxMa(code,parseDay)



