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
大概率封涨停：
* 日K光头光脚阳线；
* 较前一日缩量；
* 成交量在5日均量线之下；
* 股价处于日、周线图上涨初、中期；
'''
class BaldRiseLineAndVolumeReduceParser(BaseParser):
  _tag = 'BaldRiseLineAndVolumeReduceParser'
  
  def __init__(self,parseDay):
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


    # # 相对前一日量
    # =================================================
    # dayList = self.getPastTradingDayList(parseDay,2)
    # lastDay = dayList[0] # 前一日
    # vOfParseDay = self.getVolumeOfDay(res,parseDay)
    # vOfLastDay = self.getVolumeOfDay(res,lastDay)
    # if 0 == vOfLastDay: # 前一日无量的排除，可能是未开板次新
    #   return False

    # if vOfParseDay >= vOfLastDay: # 缩量
    # # if vOfParseDay <= vOfLastDay: # 放量
    #   return False


    # 剔除涨停
    # =================================================
    # if self.isUpwardLimit(res,dayList[0],dayList[1]):
    #   return False


    # # # 量小于5日平均
    # dayList = self.getPastTradingDayList(parseDay,5)
    # maVolume = self.getMaVolume(res,dayList)
    # if vOfParseDay>= maVolume:
    #   return False

    return True





if __name__ == '__main__':
  print 'BaldRiseLineAndVolumeReduceParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = BaldRiseLineAndVolumeReduceParser(parseDay).getParseResult(True)
  print idList

















