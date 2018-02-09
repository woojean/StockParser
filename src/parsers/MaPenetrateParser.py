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
均线穿透
'''
class MaPenetrateParser(BaseParser):
  _tag = 'MaPenetrateParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = True
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]  # 第1天
    day2 = dayList[1]  # 第2天
    #day3 = dayList[2]  # 第3天

    shortTerm = 13
    longTerm = 34
   
    # 第一天MA5小于MA60
    maLong = self.getMAPrice(res,BaseParser.getPastTradingDayList(day1,longTerm))
    maShort = self.getMAPrice(res,BaseParser.getPastTradingDayList(day1,shortTerm))
    if maShort >= maLong:
      return False

    # 第二天MA5大于MA60
    maLong = self.getMAPrice(res,BaseParser.getPastTradingDayList(day2,longTerm))
    maShort = self.getMAPrice(res,BaseParser.getPastTradingDayList(day2,shortTerm))
    if maShort < maLong:
      return False

    return ret



if __name__ == '__main__':
  print 'MaPenetrateParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaPenetrateParser(parseDay).getParseResult(True)
  print idList

















