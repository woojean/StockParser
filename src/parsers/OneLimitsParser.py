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
一板
'''
class OneLimitsParser(BaseParser):
  _tag = 'OneLimitsParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False

    dayList = BaseParser.getPastTradingDayList(parseDay,5)

    startPrice = self.getEndPriceOfDay(res,dayList[3])
    endPrice = self.getEndPriceOfDay(res,dayList[4])
    growthRate =  (endPrice-startPrice)/startPrice
    if growthRate < 0.09:
      return False

    startPrice = self.getEndPriceOfDay(res,dayList[2])
    endPrice = self.getEndPriceOfDay(res,dayList[3])
    growthRate =  (endPrice-startPrice)/startPrice
    if growthRate > 0.03:
      return False

    startPrice = self.getEndPriceOfDay(res,dayList[1])
    endPrice = self.getEndPriceOfDay(res,dayList[2])
    growthRate =  (endPrice-startPrice)/startPrice
    if growthRate > 0.03:
      return False

    startPrice = self.getEndPriceOfDay(res,dayList[0])
    endPrice = self.getEndPriceOfDay(res,dayList[1])
    growthRate =  (endPrice-startPrice)/startPrice
    if growthRate > 0.03:
      return False

    return True



if __name__ == '__main__':
  print 'OneLimitsParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = OneLimitsParser(parseDay).getParseResult(True)
  print idList

















