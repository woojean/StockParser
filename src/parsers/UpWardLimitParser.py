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
    maxPrice2 = self.getMaxPriceOfDay(res,day2)
    if maxPrice2 == startPrice2:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    if rate > 0.099:
      return True
    else:
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


    # 当日涨停
    if self._limitNum == 0: # 今日是板就OK
      if self.isUpwardLimit(res,day5,day6):
        return True
      else:
        return False
    
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

















