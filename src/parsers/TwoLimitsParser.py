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

    # 当日板了
    startPrice = self.getEndPriceOfDay(res,dayList[1])
    endPrice = self.getEndPriceOfDay(res,dayList[2])
    growthRate =  (endPrice-startPrice)/startPrice
    if growthRate < 0.095:
      return False

    # 前一日板了
    startPrice = self.getEndPriceOfDay(res,dayList[0])
    endPrice = self.getEndPriceOfDay(res,dayList[1])
    growthRate =  (endPrice-startPrice)/startPrice
    if growthRate < 0.095:
      return False
    
    print id
    if id == '300664':
      print changeRate
    changeRate = self.geChangeRateOfDay(res,parseDay)
    if changeRate > 0.15:
      return False

    return True



if __name__ == '__main__':
  print 'TwoLimitsParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = TwoLimitsParser(parseDay).getParseResult(True)
  print idList

















