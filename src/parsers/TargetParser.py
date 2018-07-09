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
“近n天x个板且未破5日线”
'''
class TargetParser(BaseParser):
  _tag = 'TargetParser'
  
  _days = 10 # 近n日
  _num = 3 # x个板

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  def isUpLimit(self,res,day):
    dayList = self.getPastTradingDayList(day,2)
    endPrice1 = self.getEndPriceOfDay(res,dayList[0])
    endPrice2 = self.getEndPriceOfDay(res,dayList[1])
    if endPrice1==0 or endPrice2 ==0:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    if rate < 0.099:
      return False
    
    return True


  def parse(self,res,parseDay,id=''):
    ret = False
    
    dayList = self.getPastTradingDayList(parseDay,self._days)

    limitNum = 0
    for day in dayList:
      if self.isUpLimit(res,day):
        limitNum += 1
    
    print limitNum

    # 板数判断
    if limitNum < self._num:
      return False

    # MA判断
    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    ma5 = self.getMAPrice(res,dayList)

    endPrice = self.getEndPriceOfDay(res,parseDay)
    if endPrice < ma5:
      return False

    return True



if __name__ == '__main__':
  print 'TargetParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = TargetParser(parseDay).getParseResult(True)
  print idList

















