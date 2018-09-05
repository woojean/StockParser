#coding:utf-8
#!/usr/bin/env python

'''
woojean@2018-08-29
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
向上穿透20日线（月线）
'''
class PenetrateUpwardMa20Parser(BaseParser):
  _tag = 'PenetrateUpwardMa20Parser'
  _days = 20

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False
    
    # 取参数
    parseDayStartPrice = self.getStartPriceOfDay(res,parseDay)
    parseDayEndPrice = self.getEndPriceOfDay(res,parseDay)
    parseDayMinPrice = self.getMinPriceOfDay(res,parseDay)
    parseDayMaxPrice = self.getMaxPriceOfDay(res,parseDay)
    if parseDayStartPrice == 0 or parseDayEndPrice == 0 or parseDayMinPrice == 0 or parseDayMaxPrice == 0:
      return False

    
    # 当日阳线
    # if parseDayEndPrice < parseDayStartPrice:
    #   return False


    # 当日收盘价在MA之上
    maDayList = BaseParser.getPastTradingDayList(parseDay,self._days)
    (v,v,parseDayMa) = self.getMAPrice(res,maDayList)
    if parseDayEndPrice <= parseDayMa:
      return False


    # MA处于当日K线下半部
    # rate = (parseDayMa - parseDayMinPrice)/(parseDayMaxPrice - parseDayMinPrice)
    # if rate > 0.5:
    #   return False

    
    # 当日非涨停（不参与打板行情，只做正常发展的趋势）
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # endPrice1 = self.getEndPriceOfDay(res,dayList[0])
    # if endPrice1 == 0:
    #   return False
    # gr =  (parseDayEndPrice-endPrice1)/endPrice1
    # if gr > 0.09:
    #   return False


    # 不在季线附近
    # boundRate = 0.03  # 
    # bigMaDayList = BaseParser.getPastTradingDayList(parseDay,60)  # 季线
    # (v,v,bigMa) = self.getMAPrice(res,bigMaDayList)
    # bigMaLowBound = bigMa*(1-boundRate)
    # bigMaUpBound = bigMa*(1+boundRate)
    # # if (parseDayEndPrice > bigMaLowBound) and (parseDayEndPrice < bigMaUpBound):
    # if (parseDayMaxPrice > bigMaLowBound) and (parseDayMaxPrice < bigMaUpBound):
    #   return False
    # if (parseDayMinPrice > bigMaLowBound) and (parseDayMinPrice < bigMaUpBound):
    #   return False


    # 不在年线附近
    # boundRate = 0.03  # 
    # bigMaDayList = BaseParser.getPastTradingDayList(parseDay,250) # 年线
    # (v,v,bigMa) = self.getMAPrice(res,bigMaDayList)
    # bigMaLowBound = bigMa*(1-boundRate)
    # bigMaUpBound = bigMa*(1+boundRate)
    # # if (parseDayEndPrice > bigMaLowBound) and (parseDayEndPrice < bigMaUpBound):
    # if (parseDayMaxPrice > bigMaLowBound) and (parseDayMaxPrice < bigMaUpBound):
    #   return False
    # if (parseDayMinPrice > bigMaLowBound) and (parseDayMinPrice < bigMaUpBound):
    #   return False


    # 当日非长上引线
    # startPrice = self.getStartPriceOfDay(res,parseDay)
    # endPrice = self.getEndPriceOfDay(res,parseDay)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if startPrice == 0 or endPrice == 0 or minPrice == 0 or maxPrice == 0:
    #   return False
    # rate = (maxPrice - max(startPrice,endPrice))/(maxPrice - minPrice)
    # if rate > 0.5:
    #   return False

    
    # 前几日最高价都在ma之下
    n = 1
    pastDayList = BaseParser.getPastTradingDayList(parseDay,n+1)  # 过去5日收盘都在20日线之下
    pastDayList = pastDayList[:-1]
    for day in pastDayList:
      maDayList = BaseParser.getPastTradingDayList(day,self._days)
      (v,v,ma) = self.getMAPrice(res,maDayList)
      # endPrice = self.getEndPriceOfDay(res,day) # 前几日收盘价都在ma之下
      # if endPrice >= ma:
      #   return False
      maxPrice = self.getMaxPriceOfDay(res,day)
      if maxPrice >= ma:
        return False



    # 放量（近n日量最大）
    # parseDayVolume = self.getVolumeOfDay(res,parseDay)
    # for day in pastDayList:
    #   volume = self.getVolumeOfDay(res,day)
    #   if volume > parseDayVolume:
    #     return False

    return True



if __name__ == '__main__':
  print 'PenetrateUpwardMa20Parser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = PenetrateUpwardMa20Parser(parseDay).getParseResult(True)
  print idList

















