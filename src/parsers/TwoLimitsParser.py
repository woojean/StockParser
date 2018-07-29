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
二板
'''
class TwoLimitsParser(BaseParser):
  _tag = 'TwoLimitsParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False

    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]
    day2 = dayList[1]
    day3 = dayList[2]
    startPriceOfDay1 = self.getStartPriceOfDay(res,day1)
    endPriceOfDay1 = self.getEndPriceOfDay(res,day1)
    startPriceOfDay2 = self.getStartPriceOfDay(res,day2)
    endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
    startPriceOfDay3 = self.getStartPriceOfDay(res,day3)
    endPriceOfDay3 = self.getEndPriceOfDay(res,day3)
    if 0==startPriceOfDay1 or  0== endPriceOfDay1:
      return False
    if 0==startPriceOfDay2 or  0== endPriceOfDay2:
      return False
    if 0==startPriceOfDay3 or  0== endPriceOfDay3:
      return False

    # 0,   1,   2
    # day1 day2 day3
    # 当日非一字板
    rate = (endPriceOfDay3 - startPriceOfDay3)/startPriceOfDay3
    if rate  < 0.005:
      return False


    # 当日板了，day3即当日
    gr2 =  (endPriceOfDay3-endPriceOfDay2)/endPriceOfDay2
    if gr2 < 0.099:
      return False


    # 前一日板了
    gr1 =  (endPriceOfDay2-endPriceOfDay1)/endPriceOfDay1
    if gr1 < 0.099:
      return False

    # 仅二连板
    # dayList = BaseParser.getPastTradingDayList(day1,2)
    # endPriceOfDay0 = self.getEndPriceOfDay(res,dayList[0])
    # if 0==endPriceOfDay0:
    #   return False
    # gr0 = (endPriceOfDay1-endPriceOfDay0)/endPriceOfDay0
    # if gr0 > 0.099:
    #   return False

    # changeRate = self.geChangeRateOfDay(res,parseDay)
    # if changeRate > 0.15:
    #   return False

    return True



if __name__ == '__main__':
  print 'TwoLimitsParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = TwoLimitsParser(parseDay).getParseResult(True)
  print idList

















