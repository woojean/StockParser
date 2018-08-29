#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-07-23
'''

import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime
from BaseParser import BaseParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
“近n天最低价大于MA（这样才能“回踩”）”
'''
class MinPriceMoreThanMaParser(BaseParser):
  _tag = 'MinPriceMoreThanMaParser'
  days = 1  # 连续n日
  maDays = 5  # n日均线
  minGr = -0.00  # 最小跌幅
  maxGr = -0.1  # 最大跌幅 
  advance = 0.000 # 提前量
  accurate = False # 是否精确要求

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def isInMaTrend(self,res,day):
    R = 5
    G = 10
    B = 20

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if not ((maR > maG) and (maG > maB)):
      return False

    return True



  def computeGr(self,res,parseDay):
    dayList = self.getPastTradingDayList(parseDay,4)
    e1 = self.getEndPriceOfDay(res,dayList[0])
    e2 = self.getEndPriceOfDay(res,dayList[1])
    e3 = self.getEndPriceOfDay(res,dayList[2])
    e4 = self.getEndPriceOfDay(res,dayList[3])
    s4 = e1 + e2 + e3 + e4

    if 0 == e1*e2*e3*e4:
      gr5 = -1
      b = 0
    else:
      gr5 = s4/(4*e4) - 1
      e5 = (1 + gr5) * e4
      b = (1 + gr5 + self.advance) * e4 # 买入价
      gr5 = round(gr5,4)
    return (gr5,b)


  def parse(self,res,parseDay,id=''):
    ret = True
    if not self.isInMaTrend(res,parseDay):
      return False

    dayList = self.getPastTradingDayList(parseDay,self.days+1)

    preDay = dayList[0]
    if self.accurate:
      maDayList = self.getPastTradingDayList(preDay,self.maDays)
      (v,v,ma) = self.getMAPrice(res,maDayList)
      minPrice = self.getMinPriceOfDay(res,preDay)
      if ma == -1:
        return False
      if minPrice == 0:
        return False
      if minPrice > ma:
        return False

    dayList = dayList[1:]
    for day in dayList:
      maDayList = self.getPastTradingDayList(day,self.maDays)
      (v,v,ma) = self.getMAPrice(res,maDayList)
      minPrice = self.getMinPriceOfDay(res,day)

      if ma == -1:
        ret = False
        break
      if minPrice == 0:
        ret = False
        break

      if minPrice < ma:
        ret = False
        break

    (gr,b) = self.computeGr(res,parseDay) # 计算预期跌幅和预期买入价
    if (gr > self.minGr) or (gr < self.maxGr):
      ret = False

    # if not ((-0.03 > gr > -0.04) or (-0.06 > gr > -0.07)):
      # ret = False
    
    if ret:
      print id,str(gr*100.0)+"%",b    

    return ret

# ==================================================================



if __name__ == '__main__':
  print 'MinPriceMoreThanMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MinPriceMoreThanMaParser(parseDay).getParseResult(True)
  print idList

















