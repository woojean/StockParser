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

  def parse(self,res,parseDay,id=''):
    ret = False

    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)

    # 必须为阳线
    if endPrice <= startPrice:
      return False

    # 必须光头
    if maxPrice > endPrice:
      return False

    # 必须光脚
    if minPrice < startPrice:
      return False

    # 相对前一日缩量
    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0] # 前一日
    vOfParseDay = self.getVolumeOfDay(res,parseDay)
    vOfLastDay = self.getVolumeOfDay(res,lastDay)
    if vOfParseDay >= vOfLastDay:
      return False


    # 量小于5日平均
    dayList = self.getPastTradingDayList(parseDay,5)
    maVolume = self.getMaVolume(res,dayList)
    if vOfParseDay>= maVolume:
      return False

    return True


if __name__ == '__main__':
  print 'BaldRiseLineAndVolumeReduceParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = BaldRiseLineAndVolumeReduceParser(parseDay).getParseResult(True)
  print idList

















