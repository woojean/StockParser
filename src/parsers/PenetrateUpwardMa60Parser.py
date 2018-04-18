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
向上穿透60日线
'''
class PenetrateUpwardMa60Parser(BaseParser):
  _tag = 'PenetrateUpwardMa60Parser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False
    
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]
    day2 = dayList[1]

    # 前一日收盘价在MA之下
    dayList = BaseParser.getPastTradingDayList(day1,60)
    (v,v,ma) = self.getMAPrice(res,dayList)
    endPrice1 = self.getEndPriceOfDay(res,day1)
    if endPrice1 >= ma:
      return False

    # 当日收盘价在MA之上
    dayList = BaseParser.getPastTradingDayList(day2,60)
    (v,v,ma) = self.getMAPrice(res,dayList)
    parseDayMa = ma
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice2 <= ma:
      return False

    return True



if __name__ == '__main__':
  print 'PenetrateUpwardMa60Parser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = PenetrateUpwardMa60Parser(parseDay).getParseResult(True)
  print idList

















