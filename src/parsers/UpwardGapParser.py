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
class UpwardGapParser(BaseParser):
  _tag = 'UpwardGapParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

  def isUpwardLimit(self,res,day1,day2):
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    # if rate > 0.099:
    if rate > 0.09:
      return True
    else:
      return False

  def isRgbBear(self,res,day):
    R = 5
    G = 10
    B = 20

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if ((maR < maG) and (maG < maB)):
      return True
    return False


  def parse(self,res,parseDay,id=''):
 
    ret = False
    dayList = self.getPastTradingDayList(parseDay,2)
    
    # 向上跳空
    # =================================================
    maxPrice1 = self.getMaxPriceOfDay(res,dayList[0])
    minPrice2 = self.getMinPriceOfDay(res,dayList[1])
    if minPrice2 == 0 or maxPrice1==0: # 剔除复牌股
      return False
    if minPrice2 <= maxPrice1:
      return False
    
    # 剔除ST
    # =================================================
    name = Tools.getNameById(id)
    if 'ST' in name:
      return False


    # 剔除近10日内有过涨停板（涨幅大于9%），因为需要“沉闷”的行情
    # =================================================
    uLcDayList = self.getPastTradingDayList(parseDay,11)
    l = len(uLcDayList)
    for i in xrange(0,l-1):
      if self.isUpwardLimit(res,uLcDayList[i],uLcDayList[i+1]):
        return False


    # 剔除跳空涨停
    # =================================================
    if self.isUpwardLimit(res,dayList[0],dayList[1]):
      return False


    # 剔除新股
    # =================================================
    vOfLastDay = self.getVolumeOfDay(res,dayList[0])
    if 0 == vOfLastDay: # 前一日无量的排除，可能是未开板次新
      return False

    # 排除短线空头排列
    # =================================================
    if self.isRgbBear(res,parseDay):
      return False


    # 剔除上引线长度超过总线长度2/3
    # =================================================
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    upLine = abs(maxPrice - max(startPrice,endPrice))
    totalLine = abs(maxPrice - minPrice)
    if totalLine!=0:
      rate = 1.0*upLine/totalLine
      if rate > 0.667:
        return False


    # 且剔除K线长度超过近10日K线长度平均值：《日本蜡烛图技术》
    # =================================================
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    kLineLength = abs(maxPrice - minPrice)
    totalLineLength = 0
    total = 10
    klDayList = self.getPastTradingDayList(parseDay,total+1)
    klDayList = klDayList[:-1]
    for d in klDayList:
      minPrice = self.getMinPriceOfDay(res,d)
      maxPrice = self.getMaxPriceOfDay(res,d)
      lineLength = abs(maxPrice - minPrice)
      totalLineLength += lineLength
    avgLength = totalLineLength/total
    if kLineLength > avgLength:
      return False

    return True



if __name__ == '__main__':
  print 'UpwardGapParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = UpwardGapParser(parseDay).getParseResult(True)
  print idList

















