#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-11-21
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
from KdjParser import KdjParser
from BiasParser import BiasParser
from common import Tools
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
突破
'''
class BreakthroughParser(BaseParser):
  _tag = 'BreakthroughParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  


  def parse(self,res,parseDay,id=''):
    data = {}
    dayList = BaseParser.getPastTradingDayList(self._parseDay,100)

    endPrice = self.getEndPriceOfDay(res,self._parseDay)
    lastDayEndPrice = self.getMaxPriceOfDay(res,dayList[-2])

    startDay = ''
    peakDay = ''
    leftInterval = 0
    rightInterval = 0
    total = len(dayList)

    # 寻找区间顶
    for i in xrange(3,total-1):  # 从-3开始
      maxPrice = self.getMaxPriceOfDay(res,dayList[-i])
      if maxPrice >= endPrice:  # 最高价已超过当日收盘价，突破已不存在
        break
      if maxPrice > lastDayEndPrice:
        peakDay = dayList[-i] # 区间顶
        rightInterval = i-1
        break
      if '' == peakDay:
        return False

    # 确定左边区间
    peakDayMaxPrice = self.getMaxPriceOfDay(res,peakDay)
    dayList = BaseParser.getPastTradingDayList(peakDay,100)
    total = len(dayList)
    for i in xrange(2,total-1): 
      maxPrice = self.getMaxPriceOfDay(res,dayList[-i])
      if maxPrice > peakDayMaxPrice:
        startDay = dayList[-i]
        leftInterval = i
        break
      if '' == startDay:
        return False

      if leftInterval < minLeftInterval:
        return False

      if rightInterval < minRightInterval:
        return False
    return True


minLeftInterval = 10
minRightInterval = 10

if __name__ == '__main__':
  print 'BreakthroughParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = BreakthroughParser(parseDay).getParseResult(True)
  print idList

















