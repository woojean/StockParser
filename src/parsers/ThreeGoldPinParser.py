#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-07
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
三针探底
'''
class GoldenPinBottomParser(BaseParser):
  _tag = 'GoldenPinBottomParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  def isGoldPin(self,res,parseDay):
    ret = False
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)

    downLine = abs(minPrice - min(startPrice,endPrice))
    totalLine = abs(maxPrice - minPrice)

    # 去掉无下引线的
    if totalLine == 0: 
      return False

    # 下引线相对长度（按《日本蜡烛图技术》的定义，至少2倍，这里适度放松）
    rate = downLine/totalLine
    if rate < 0.7:
      return False

    return True


  def isMaInBear(self,res,day):
    R = 5
    G = 10
    B = 20

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if maR == -1 or maG==-1 or maB == -1:
      return False

    if ((maR < maG) and (maG < maB)):
      return True
    return False



  def parse(self,res,parseDay,id=''):
    # 换手率>1%
    cr = self.getChangeRateOfDay(res,parseDay)
    if cr < 0.01:
      return False


    # 连续3天长下引线
    dayList = self.getPastTradingDayList(parseDay,3)
    for day in dayList:
      if not self.isGoldPin(res,day):
        return False

    # 再往前一日不是长下引线（太多了，没有意义）
    dayList = self.getPastTradingDayList(parseDay,4)
    day = dayList[0]
    if self.isGoldPin(res,day):
      return False

    
    # 短线空头排列
    if not self.isMaInBear(res,parseDay):
      return False

    # 近3日的最高的针是近20日的最低价
    dayList = self.getPastTradingDayList(parseDay,3)
    minPrice1 = self.getMinPriceOfDay(res,dayList[0])
    minPrice2 = self.getMinPriceOfDay(res,dayList[1])
    minPrice3 = self.getMinPriceOfDay(res,dayList[2])
    minPrice = max(minPrice1,minPrice2,minPrice3)

    dayList = self.getPastTradingDayList(parseDay,23)
    dayList = dayList[:-3]
    for day in dayList:
      price = self.getMinPriceOfDay(res,parseDay)
      if price < minPrice:
        return False

    return True


if __name__ == '__main__':
  print 'GoldenPinBottomParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = GoldenPinBottomParser(parseDay).getParseResult(True)
  print idList

















