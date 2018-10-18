#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-18
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
基于阴阳线数量
'''
class YinYangParser(BaseParser):
  _tag = 'YinYangParser'
  
  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 

  
  def isYang(self,res,parseDay):
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if startPrice ==0 or endPrice == 0:
      return False

    # print endPrice,startPrice
    if endPrice > startPrice:
      return True
    else:
      return False


  def parse(self,res,parseDay,id=''):
    # print id
    days = 20
    maxYangNum = 5
    yangNum = 0

    dayList = self.getPastTradingDayList(parseDay,days)
    for day in dayList:
      endPrice = self.getEndPriceOfDay(res,day)
      if endPrice == 0:  # 过滤无交易的股
        yangNum = 999
        break
      if self.isYang(res,day):
        yangNum += 1
    
    # print yangNum,maxYangNum
    if yangNum > maxYangNum:
      return False

    return True


if __name__ == '__main__':
  print 'YinYangParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = YinYangParser(parseDay).getParseResult(True)
  print idList

















