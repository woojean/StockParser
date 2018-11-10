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
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
涨停板
'''
class UpWardLimitParser(BaseParser):
  _tag = 'UpWardLimitParser'
  _limitNum = 0
  
  def __init__(self,limitNum,parseDay):
    self._limitNum = limitNum
    BaseParser.__init__(self,parseDay) 


  def isUpwardLimit(self,res,day1,day2):
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0:
      return False

    # 排除一字板
    startPrice2 = self.getStartPriceOfDay(res,day2)
    minPrice2 = self.getMinPriceOfDay(res,day2)
    maxPrice2 = self.getMaxPriceOfDay(res,day2)
    if maxPrice2 == minPrice2 and startPrice2 == minPrice2:
      return False


    rate = (endPrice2 - endPrice1)/endPrice1
    if rate > 0.099:
      return True
    else:
      return False
    

  def isDownLimit(self,res,day1,day2):
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    if rate <= -0.099:
      return True
    else:
      return False
  

  def isMaInBear(self,res,day):
    R = 5
    G = 10
    B = 20

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if maR == -1 or maG==-1 or maB == -1:
      return False

    if ((maR < maG) and (maG < maB)):
      return True
    return False


  def parse(self,res,parseDay,id=''):
    ret = False
    
    # day1,day2,day3,day4,day5,day6
    dayList = BaseParser.getPastTradingDayList(parseDay,6)
    day1 = dayList[0]
    day2 = dayList[1]
    day3 = dayList[2]
    day4 = dayList[3]
    day5 = dayList[4]
    day6 = dayList[5]

    # 最低价低于5日线
    # maDayList = BaseParser.getPastTradingDayList(parseDay,5)
    # (v,v,ma) = self.getMAPrice(res,maDayList)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # if minPrice > ma:
    #   return False
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if maxPrice > ma:
    #   return False

    
    # 近5日内有跌停
    # haveDownwardLimit = False
    # cDayList = BaseParser.getPastTradingDayList(parseDay,6)
    # total = len(cDayList)
    # for i in xrange(0,total-2):
    #   if self.isDownLimit(res,cDayList[i],cDayList[i+1]):
    #     haveDownwardLimit = True
    #     break
    # if not haveDownwardLimit:
    #   return False

    
    # 短线均线空头排列
    # if not self.isMaInBear(res,dayList[-2]):
    #   return False


    # 当日涨停
    if self._limitNum == 0: # 今日是板就OK
      if not self.isUpwardLimit(res,day5,day6):
        return False
      
      # 跳空涨停
      # minPrice6 = self.getMinPriceOfDay(res,day6)
      # maxPrice5 = self.getMaxPriceOfDay(res,day5)
      # # print id,minPrice6,maxPrice5
      # if minPrice6 <= maxPrice5:
      #   return False

      endPrice5 = self.getEndPriceOfDay(res,day5)
      endPrice6 = self.getEndPriceOfDay(res,day6)

      # # # 10天内涨幅低于20%
      # dayList = BaseParser.getPastTradingDayList(day6,10)
      # endPrice1 = self.getEndPriceOfDay(res,dayList[0])
      # if endPrice1 == 0:
      #   return False
      # rate = (endPrice6 - endPrice1)/endPrice1
      # if rate >0.2:
      #   return False


      # 当日上穿60日线
      # dayList = BaseParser.getPastTradingDayList(day6,60)
      # (v,v,ma) = self.getMAPrice(res,dayList)
      # if not (endPrice5 < ma and endPrice6 > ma):
      #   return False


      # 收盘价为近55日内最高价
      # if not self.isMaxPriceOfDays(res,parseDay,55):
      #   return False

        
      # 前一日最低价是近20日最低价
      # if not self.haveMinPriceOfDays(res,day5,20):
      #   return False


      # 近5日最低价是近55日最低价
      # if not self.intervalMinPriceOfDays(res,parseDay,5,55):
      #   return False


      # 如果收盘价在年线之下，距离年线距离在20%之上
      # dayList = BaseParser.getPastTradingDayList(day6,250)
      # (v,v,ma) = self.getMAPrice(res,dayList)
      # if ma > endPrice6:
      #   rate = (ma - endPrice6)/endPrice6
      #   if rate <0.2:
      #     return False


      return True

    
    # 仅1板
    if self._limitNum == 1: 
      if self.isUpwardLimit(res,day5,day6)\
        and (not self.isUpwardLimit(res,day4,day5)):
        return True
      else:
        return False

    # 仅2板
    if self._limitNum == 2: 
      if self.isUpwardLimit(res,day5,day6)\
        and self.isUpwardLimit(res,day4,day5)\
        and (not self.isUpwardLimit(res,day3,day4)):
        return True
      else:
        return False

    # 仅3板
    if self._limitNum == 3: 
      if self.isUpwardLimit(res,day5,day6) \
        and self.isUpwardLimit(res,day4,day5)\
        and self.isUpwardLimit(res,day3,day4)\
        and (not self.isUpwardLimit(res,day2,day3)):
        return True
      else:
        return False
    
    # 仅4板
    if self._limitNum == 4: 
      if self.isUpwardLimit(res,day5,day6) \
        and self.isUpwardLimit(res,day4,day5)\
        and self.isUpwardLimit(res,day3,day4)\
        and self.isUpwardLimit(res,day2,day3)\
        and (not self.isUpwardLimit(res,day1,day2)):
        return True
      else:
        return False

    

    return True

# ===========================================================
limitNum = 1 # 0 无限制，1 仅限1板，2 仅限2板


if __name__ == '__main__':
  print 'UpWardLimitParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = UpWardLimitParser(limitNum,parseDay).getParseResult(True)
  print idList

















