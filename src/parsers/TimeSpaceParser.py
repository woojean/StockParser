#coding:utf-8
#!/usr/bin/env python
'''
woojean@2019-04-10
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
时空解析
'''
class TimeSpaceParser(BaseParser):
  _tag = 'TimeSpaceParser'

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def getTimeSpaceData(self,res,parseDay):
    minDays = 60
    maxSpace = 0.3
    dayList = self.getPastTradingDayList(parseDay,250)
    dayList.reverse()
    dayList = dayList[1:]  # 去掉当日

    days = 1
    maxPriceOfDays = self.getMaxPriceOfDay(res,parseDay)
    minPriceOfDays = 9999  # 区间最低价
    startDay = parseDay
    for day in dayList:
      maxP = self.getMaxPriceOfDay(res,day)
      if maxP == 0: # 停牌
          continue
      if maxP < maxPriceOfDays: 
        days += 1  # 时间+1
        minP = self.getMinPriceOfDay(res,day)
        if minP < minPriceOfDays:
          minPriceOfDays = minP  # 空间向下拓展
        startDay = day
      else: # 结束
        break

    if days < 60:
      return False
    
    if minPriceOfDays == 0:
      return False
    space = (maxPriceOfDays - minPriceOfDays)/minPriceOfDays
    if space > 0.3:
      return False
      
    return [days,space,startDay,parseDay]




  def parse(self,res,parseDay,id=''):
    timeSpaceData = self.getTimeSpaceData(res,parseDay)
    if False == timeSpaceData:
      return False
    
    print id
    print timeSpaceData

    return True
    



if __name__ == '__main__':
  print 'TimeSpaceParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = TimeSpaceParser(parseDay).getParseResult(True)
  print idList

















