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
MaTrend From ZLG
'''
class MaTrendParser(BaseParser):
  _tag = 'MaTrendParser'
  
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

  def haveEndPriceDecline(self,res,parseDay,days):
    ret = False
    dayList = self.getPastTradingDayList(parseDay,days+1)
    for i in xrange(1,days):  # 从第2项开始判断
      endPrice1 = self.getEndPriceOfDay(res,dayList[i-1])
      endPrice2 = self.getEndPriceOfDay(res,dayList[i])
      if endPrice2 < endPrice1:
        ret = True
        break
    return ret


  def haveDeclineLine(self,res,parseDay,days):
    ret = False
    dayList = self.getPastTradingDayList(parseDay,days)
    for i in xrange(0,days):  # 从第2项开始判断
      startPrice = self.getStartPriceOfDay(res,dayList[i])
      endPrice = self.getEndPriceOfDay(res,dayList[i])
      if endPrice <= startPrice:
        ret = True
        break
    return ret


  def isEndPriceHigher(self,res,parseDay,days):
    ret = True
    dayList = self.getPastTradingDayList(parseDay,days)
    endPrice1 = self.getEndPriceOfDay(res,dayList[0])
    endPrice2 = self.getEndPriceOfDay(res,parseDay)
    if endPrice2 < endPrice1:
      ret =  False
    return ret


  def parse(self,res,parseDay,id=''):
    # 最近10天，5、10、20日均线多头排列
    dayList = self.getPastTradingDayList(parseDay,10)
    isInTrend = True
    for d in dayList:
      if not self.isInMaTrend(res,d) :
        isInTrend = False
        break

    if not isInTrend:
      return False

    # 最近3天出现过价格下跌或者阴线
    if ((not self.haveEndPriceDecline(res,parseDay,3)) and (not self.haveDeclineLine(res,parseDay,3))):
      return False

    # 当日收在5日线之上
    dayList = self.getPastTradingDayList(parseDay,5)
    (v,v,ma5) = self.getMAPrice(res,dayList)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if endPrice < ma5:
      return False

    # 当日阳线
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if endPrice < startPrice:
      return False


    # 收盘价大于30天之前的收盘价
    if not self.isEndPriceHigher(res,parseDay,30):
      return False

    # 收盘价大于60天之前的收盘价
    if not self.isEndPriceHigher(res,parseDay,60):
      return False

    # 收盘价大于90天之前的收盘价
    if not self.isEndPriceHigher(res,parseDay,90):
      return False

    return True
    



if __name__ == '__main__':
  print 'MaTrendParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaTrendParser(parseDay).getParseResult(True)
  print idList

















