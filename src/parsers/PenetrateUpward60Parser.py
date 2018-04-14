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
class PenetrateUpward60Parser(BaseParser):
  _tag = 'PenetrateUpward60Parser'
  
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

    # 当日MA大于5，20日、60日、120前MA（用于确定上升趋势）
    dayList = BaseParser.getPastTradingDayList(parseDay,120)
    day1 = dayList[0]
    day2 = dayList[59]
    day3 = dayList[99]
    day4 = dayList[114]

    (v,v,ma1) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day1,60))
    if parseDayMa < ma1:
      return False

    (v,v,ma2) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day2,60))
    if parseDayMa < ma2:
      return False

    (v,v,ma3) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day3,60))
    if parseDayMa < ma3:
      return False

    (v,v,ma4) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day4,60))
    if parseDayMa < ma4:
      return False


    return True



if __name__ == '__main__':
  print 'PenetrateUpward60Parser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = PenetrateUpward60Parser(parseDay).getParseResult(True)
  print idList

















