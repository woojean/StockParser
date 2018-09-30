#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-09-29
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

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools


'''
'''
class GeneralParser(BaseParser):
  _tag = 'GeneralParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 



  def isUpwardLimit(self,res,day1,day2):
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    if rate > 0.099:
      return True
    else:
      return False



  def parse(self,res,parseDay,id=''):
    ret = False

    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    
    # 关头光脚阳线
    # =================================================
    # 必须为阳线
    if endPrice <= startPrice:
      return False

    # 必须光头
    if maxPrice > endPrice:
      return False

    # 必须光脚
    if minPrice < startPrice:
      return False


    # 剔除涨停
    # =================================================
    if self.isUpwardLimit(res,dayList[0],dayList[1]):
      return False


    # # 相对前一日量
    # =================================================
    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0] # 前一日
    vOfParseDay = self.getVolumeOfDay(res,parseDay)
    vOfLastDay = self.getVolumeOfDay(res,lastDay)
    if 0 == vOfLastDay: # 前一日无量的排除，可能是未开板次新
      return False

    if vOfParseDay >= vOfLastDay: # 缩量
    # if vOfParseDay <= vOfLastDay: # 放量
      return False


    # # # 量小于5日平均
    # dayList = self.getPastTradingDayList(parseDay,5)
    # maVolume = self.getMaVolume(res,dayList)
    # if vOfParseDay>= maVolume:
    #   return False

    return True



if __name__ == '__main__':
  print 'GeneralParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = GeneralParser(parseDay).getParseResult(True)
  print idList

















