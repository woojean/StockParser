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
“吞没线”
'''
class SwallowUpParser(BaseParser):
  _tag = 'SwallowUpParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]  # 第一天
    day2 = dayList[1]  # 第二天
    day3 = dayList[2]  # 第二天
    
    startPriceOfDay1 = self.getStartPriceOfDay(res,day1)
    endPriceOfDay1 = self.getEndPriceOfDay(res,day1)
    entityOfDay1 = abs(startPriceOfDay1 - endPriceOfDay1)
    startPriceOfDay2 = self.getStartPriceOfDay(res,day2)
    endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
    entityOfDay2 = abs(startPriceOfDay2 - endPriceOfDay2)
    startPriceOfDay3 = self.getStartPriceOfDay(res,day3)
    endPriceOfDay3 = self.getEndPriceOfDay(res,day3)
    entityOfDay3 = abs(startPriceOfDay2 - endPriceOfDay3)

    # 第2天阴线
    if endPriceOfDay2 > startPriceOfDay2:
      return False

    # 第3天阳线
    if endPriceOfDay3 <= startPriceOfDay3:
      return False
  
    # 第3天实体长度是第2天的2倍
    if (entityOfDay2 != 0) and (entityOfDay3/entityOfDay2 < 2):
      return False

    # 第3天开盘低于第2天收盘
    if endPriceOfDay2 < startPriceOfDay3:
      return False

    # 第3天收盘大于第2天开盘
    if endPriceOfDay3 <= startPriceOfDay2:
      return False
   
    # 第3天同时吞没第1天
    if min(startPriceOfDay3,endPriceOfDay3) >= min(startPriceOfDay1,endPriceOfDay1):
      return False
    if max(startPriceOfDay3,endPriceOfDay3) <= max(startPriceOfDay1,endPriceOfDay1):
      return False

    return True



if __name__ == '__main__':
  print 'SwallowUpParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = SwallowUpParser(parseDay).getParseResult(True)
  print idList

















