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
from KdjParser import KdjParser
from BiasParser import BiasParser
from MaxPriceUnderMaParser import MaxPriceUnderMaParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
'''
class DailyParser(BaseParser):
  _tag = 'DailyParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def parse(self,res,parseDay,id=''):
    # 剔除新股
    if self.isNewStock(res,parseDay):
      return False

    # 阳线
    if not self.isYangXian(res,parseDay):
      return False

    # 最高价低于5日线
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if maxPrice > ma:
    #   return False


    # 振幅
    am = self.getAm(res,parseDay)
    if am < 0.05:
      return False


    # D低于
    d = KdjParser.getD(parseDay,id)
    if False == d:
      return False
    if d >= 20:
      return False
      

    return True


if __name__ == '__main__':
  print 'DailyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList


