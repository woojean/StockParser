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
“金针探底”，也即《日本蜡烛图技术》中所谓的锤子线
'''
class GoldenPinBottomParser(BaseParser):
  _tag = 'GoldenPinBottomParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  def parse(self,res,parseDay,id=''):
    ret = False
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)

    upLine = abs(maxPrice - max(startPrice,endPrice))
    downLine = abs(minPrice - min(startPrice,endPrice))
    entity = abs(endPrice - startPrice)

    # 去掉无下引线的
    if downLine == 0: 
      return False

    # 去掉有上引线的
    if upLine > 0: 
      return False

    # 下引线相对长度（按《日本蜡烛图技术》的定义，至少2倍，这里适度放松）
    rate = downLine/entity
    if id =='002606':
      print rate
    if rate < 1.618:
      return False
    
    # 触及5日最低价（用于排除上吊线）
    if not self.isMinPriceOfDays(res,parseDay,5):
      return False

    # 当日MA大于20日、60日、120前MA（用于确定上升趋势）
    dayList = BaseParser.getPastTradingDayList(parseDay,60)
    (v,v,ma) = self.getMAPrice(res,dayList)
    parseDayMa = ma
    if parseDayMa<0: # -1
      return False

    dayList = BaseParser.getPastTradingDayList(parseDay,120)
    day1 = dayList[0]
    day2 = dayList[59]
    day3 = dayList[99]

    (v,v,ma1) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day1,60))
    if parseDayMa < ma1:
      return False

    (v,v,ma2) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day2,60))
    if parseDayMa < ma2:
      return False

    (v,v,ma3) = self.getMAPrice(res,BaseParser.getPastTradingDayList(day3,60))
    if parseDayMa < ma3:
      return False

    return True


if __name__ == '__main__':
  print 'GoldenPinBottomParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = GoldenPinBottomParser(parseDay).getParseResult(True)
  print idList

















