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
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
'''
class DailyParser(BaseParser):
  _tag = 'DailyParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def parse(self,res,parseDay,id=''):
    maDays = 5

    # # 取参
    # dayList = BaseParser.getPastTradingDayList(parseDay,maDays)
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # startPrice = self.getStartPriceOfDay(res,parseDay)
    # endPrice = self.getEndPriceOfDay(res,parseDay)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # startPriceOfLastDay = self.getStartPriceOfDay(res,dayList[-2])
    # endPriceOfLastDay = self.getEndPriceOfDay(res,dayList[-2])
    # minPriceOfLastDay = self.getMinPriceOfDay(res,dayList[-2])
    # maxPriceOfLastDay = self.getMaxPriceOfDay(res,dayList[-2])

    # # 参数校验
    # if startPrice ==0 or endPrice ==0 or minPrice ==0 or maxPrice ==0:
    #   return False
    # if ma < 0:
    #   return False

    # #############################################################################
    # # 阳线
    # if endPrice <= startPrice:
    #   return False

    # # 收盘价位于ma之下
    # if endPrice >= ma:
    #   return False

    # # 振幅
    # r = (maxPrice - minPrice)/minPrice
    # if (r < 0.05):
    #   return False

    # D低于20
    # d = KdjParser.getD(parseDay,id)
    # if d >= 20:
    #   return False

    return True


if __name__ == '__main__':
  print 'DailyParser'
  print '收盘价位于5日线下，阳线，振幅超过5%'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList


