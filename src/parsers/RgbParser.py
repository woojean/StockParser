#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-06
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
from common import Tools
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
RGB
'''
class RgbParser(BaseParser):
  _tag = 'RgbParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 
  

  # =====================================================================================================
  # APIs
  # =====================================================================================================
  @staticmethod
  def getMaData(parseDay,id,days):
    path = Tools.getMaDataPath()+'/' +id
    try:
      res = open(path,'r').read()
      if len(res) < 50:
        return False 
      dayList = BaseParser.getPastTradingDayList(parseDay,days)
      maList = eval(res[26:-1])
      dataOfDays = {}
      for item in maList:
        for d in dayList:
          if d == item['time']:
            dataOfDays[d] = eval(item['ma'])
    except Exception, e:
      # pass
      # print repr(e)
      return False

    # 数据错误，当做无死叉，人工判断
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False
    return dataOfDays




  def isRgb(self,res,day):
    days = 1
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    dataOfDays = RgbParser.getMaData(parseDay,id,days)
    if False == dataOfDays:
      return False

    maR = float(dataOfDays[dayList[-1]][0]) # 5
    maG = float(dataOfDays[dayList[-1]][1]) # 10
    maB = float(dataOfDays[dayList[-1]][2]) # 20

    if not ((maR > maG) and (maG > maB)):
      return False

    return True


  def isIntervalRgb(self,res,parseDay,rgbDays,id=''):
    # 连续N天RGB
    dayList = RgbParser.getPastTradingDayList(parseDay,rgbDays)
    dataOfDays = RgbParser.getMaData(parseDay,id,rgbDays)
    if False == dataOfDays:
      return False

    for day in dayList:
      maR = float(dataOfDays[day][0]) # 5
      maG = float(dataOfDays[day][1]) # 10
      maB = float(dataOfDays[day][2]) # 20
      if not ((maR > maG) and (maG > maB)):
        return False
    return True


  def isIntervalNoMinPriceUnderMa(self,res,parseDay,days,maDays,id=''):
    # 连续N天R最低价在某条均线之上
    dayList = RgbParser.getPastTradingDayList(parseDay,days)
    dataOfDays = RgbParser.getMaData(parseDay,id,days)
    if False == dataOfDays:
      return False
    for day in dayList:
      if maDays == 5:
        ma = float(dataOfDays[day][0]) # 5
      elif maDays == 10:
        ma = float(dataOfDays[day][1]) # 10
      elif maDays == 20:
        ma = float(dataOfDays[day][2]) # 10
      minPrice = self.getMinPriceOfDay(res,day)
      if minPrice < ma:
        return False
    return True



  def parse(self,res,parseDay,id=''):
    dayList = RgbParser.getPastTradingDayList(parseDay,2)
    lastDay = dayList[-2]  # 信号日前一日

    # 连续N天RGB（仍然多头排列，趋势还在）
    rgbDays = 5 # 连续N日RGB
    if not self.isIntervalRgb(res,parseDay,rgbDays,id):
      return False

    maData = self.getMaData(parseDay,id,1)[parseDay]
    ma20 = float(maData[2])

    
    # 当日收盘价高于20日均线（未跌破）
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if endPrice <= ma20:
      return False

    # 当日最低价与20日均线很近（当天挑战过20日均线，且弹回）
    absRate = 0.02
    minPrice = self.getMinPriceOfDay(res,parseDay)
    value = abs(1 - minPrice/ma20)
    if value > absRate:
      return False

    
    # 截止昨日连续N天最低价在ma之上（之前未挑战过20日均线，即初次挑战）
    # maDays = 5
    # if not self.isIntervalNoMinPriceUnderMa(res,lastDay,rgbDays,maDays,id):
    #   return False

    return True
    



if __name__ == '__main__':
  print 'RgbParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = RgbParser(parseDay).getParseResult(True)
  print idList

















