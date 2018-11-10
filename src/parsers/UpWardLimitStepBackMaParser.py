#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-11-08
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
涨停板，首次回踩5日线
'''
class UpWardLimitStepBackMaParser(BaseParser):
  _tag = 'UpWardLimitStepBackMaParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 


  @staticmethod
  def getReboundMa5(res,parseDay):
    parser = BaseParser(parseDay)
    dayList = parser.getPastTradingDayList(parseDay,4)
    e1 = parser.getEndPriceOfDay(res,dayList[0])
    e2 = parser.getEndPriceOfDay(res,dayList[1])
    e3 = parser.getEndPriceOfDay(res,dayList[2])
    e4 = parser.getEndPriceOfDay(res,dayList[3])
    s4 = e1 + e2 + e3 + e4

    if 0 == e1*e2*e3*e4:
      return -1
    gr5 = s4/(4*e4) - 1

    return gr5

  

  # 是否涨停（含一字板）
  def isUpwardLimit(self,res,day1,day2):
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    if rate > 0.097:
      return True
    else:
      return False
   

  def parse(self,res,parseDay,id=''):

    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    endPrice = self.getEndPriceOfDay(res,parseDay)

	# 必须秃顶（一字板 或 T字板）
    startP = self.getStartPriceOfDay(res,parseDay)
    minP = self.getMinPriceOfDay(res,parseDay)
    maxP = self.getMaxPriceOfDay(res,parseDay)
    if not(maxP == startP):
      return False


    # 当日涨停
    if not self.isUpwardLimit(res,dayList[-2],dayList[-1]):
      return False
	

    # 昨日涨停（至少2连板）
    # if not self.isUpwardLimit(res,dayList[-3],dayList[-2]):
    #   return False

    # 当日收盘价在MA5之上
    (v,v,ma) = self.getMAPrice(res,dayList)
    if endPrice < ma:
      return False

    # rebound ma5
    gr = UpWardLimitStepBackMaParser.getReboundMa5(res,parseDay)
    if gr <= -1:
      return False

    return True




if __name__ == '__main__':
  print 'UpWardLimitStepBackMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = UpWardLimitStepBackMaParser(parseDay).getParseResult(True)
  print idList

















