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
简单解析
60日线是一个重要位置，突破意义重大
'''
class SimpleParser(BaseParser):
  _tag = 'SimpleParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def isPenetrateMa(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,60)
    (v,v,ma) = self.getMAPrice(res,dayList)
    
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)

    if endPrice <= startPrice:
      return False

    if startPrice >= ma:
      return False

    if endPrice <= ma:
      return False

    return True
  


  def parse(self,res,parseDay,id=''):
    ret = True

    # x 2 3
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]
    day2 = dayList[1]
    day3 = dayList[2]

    # 第1日阳线、穿透均线
    if not self.isPenetrateMa(res,day1):
      return False

    dayList = BaseParser.getPastTradingDayList(day1,60)
    (v,v,ma) = self.getMAPrice(res,dayList)

    # 第2日站稳
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice2 <= ma:
      return False

    # 第2日站稳
    endPrice3 = self.getEndPriceOfDay(res,day3)
    if endPrice3 <= ma:
      return False

    return ret



if __name__ == '__main__':
  print 'SimpleParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = SimpleParser(parseDay).getParseResult(True)
  print idList

















