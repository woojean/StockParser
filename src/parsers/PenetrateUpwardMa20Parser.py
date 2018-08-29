#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-08-29
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
向上穿透20日线（月线）
'''
class PenetrateUpwardMa20Parser(BaseParser):
  _tag = 'PenetrateUpwardMa20Parser'
  _days = 20

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False
    
    # 当日收盘价在MA之上
    dayList = BaseParser.getPastTradingDayList(parseDay,self._days)
    (v,v,ma) = self.getMAPrice(res,dayList)
    parseDayMa = ma
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if endPrice <= ma:
      return False

    # 前几日收盘价都在ma之下
    pastDayList = BaseParser.getPastTradingDayList(parseDay,6)  # 过去5日收盘都在20日线之下
    pastDayList = pastDayList[:-1]
    for day in pastDayList:
      maDayList = BaseParser.getPastTradingDayList(day,self._days)
      (v,v,ma) = self.getMAPrice(res,maDayList)
      endPrice = self.getEndPriceOfDay(res,day)
      if endPrice >= ma:
        return False


    # ma处于当日K线下半部
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    rate = (parseDayMa - minPrice)/(maxPrice - minPrice)
    if rate > 0.5:
      return False
   
    '''
    无下影线的阴线
    '''


    return True



if __name__ == '__main__':
  print 'PenetrateUpwardMa20Parser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = PenetrateUpwardMa20Parser(parseDay).getParseResult(True)
  print idList

















