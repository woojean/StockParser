#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-01
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
WJ
'''
class WJParser(BaseParser):
  _tag = 'WJParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  def getMinPriceOfDays(self,res,dayList):
    price = 999999
    for day in dayList:
      minPrice = self.getMinPriceOfDay(res,day)
      if minPrice < price:
        price = minPrice
    return price

  def getMaxPriceOfDays(self,res,dayList):
    price = 0
    for day in dayList:
      maxPrice = self.getMaxPriceOfDay(res,day)
      if maxPrice > price:
        price = maxPrice
    return price


  def getAvgPriceOfDays(self,res,dayList):
    total = 0
    for day in dayList:
      price = self.getEndPriceOfDay(res,day)
      total += price
    avgPrice = total/len(dayList)
    return avgPrice


  # [开盘价，收盘价，最低价，最高价]
  def genKLines(self,res,parseDay):
    kLines = {}
    dayList = BaseParser.getPastTradingDayList(parseDay,60) # 过去一个季度
    splitList = []
    for i in xrange(0,12):
      splitList.append([i*5,(i+1)*5])

    index = 1
    for l in splitList:
      kLines[index] ={}
      kLineDayList = dayList[l[0]:l[1]]
      kLines[index]['dayList'] = kLineDayList
      kLines[index]['start'] = self.getStartPriceOfDay(res,kLineDayList[0])
      kLines[index]['end'] = self.getEndPriceOfDay(res,kLineDayList[-1])
      kLines[index]['min'] = self.getMinPriceOfDays(res,kLineDayList)
      kLines[index]['max'] = self.getMaxPriceOfDays(res,kLineDayList)
      kLines[index]['avg'] = self.getAvgPriceOfDays(res,kLineDayList)
      index += 1
    return kLines


  # 光头光脚阳线
  def isBigBaldRiseLine(self,res,parseDay):
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

    return True

  # 大阳线，且缩量
  def isBigBaldRiseLineAndVolumeReduce(self,res,parseDay):
    ret = False
    # 秃阳线
    if not self.isBigBaldRiseLine(res,parseDay):
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

    # 实体大小在最近10天排在前3
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    entity = abs(endPrice - startPrice)
    num = 0
    isEntityBigEnough = True
    dayList = self.getPastTradingDayList(parseDay,10)
    for day in dayList:
      startPriceOfDay = self.getStartPriceOfDay(res,day)
      endPriceOfDay = self.getEndPriceOfDay(res,day)
      entityOfDay = abs(endPriceOfDay - startPriceOfDay)
      if entityOfDay>entity:
        num +=1
      if num >3:
        isEntityBigEnough = False
        break
    if not isEntityBigEnough:
      return False
    

    return True 


  def isSwallowUp(self,res,parseDay):
    ret = False
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]  # 第一天
    day2 = dayList[1]  # 第二天
    day3 = dayList[2]  # 第二天
    
    startPriceOfDay1 = self.getStartPriceOfDay(res,day1)
    endPriceOfDay1 = self.getEndPriceOfDay(res,day1)
    entityOfDay1 = abs(startPriceOfDay1 - endPriceOfDay1)
    startPriceOfDay2 = self.getStartPriceOfDay(res,day2)
    endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
    entityOfDay2 = abs(startPriceOfDay2 - endPriceOfDay2)
    startPriceOfDay3 = self.getStartPriceOfDay(res,day3)
    endPriceOfDay3 = self.getEndPriceOfDay(res,day3)
    entityOfDay3 = abs(startPriceOfDay2 - endPriceOfDay3)

    # 第2天阴线
    if endPriceOfDay2 > startPriceOfDay2:
      return False

    # 第3天阳线
    if endPriceOfDay3 <= startPriceOfDay3:
      return False
  
    # 第3天实体长度是第2天的2倍
    if (entityOfDay2 != 0) and (entityOfDay3/entityOfDay2 < 2.618):
      return False

    # 第3天开盘低于第2天收盘
    if endPriceOfDay2 < startPriceOfDay3:
      return False

    # 第3天收盘大于第2天开盘
    if endPriceOfDay3 <= startPriceOfDay2:
      return False
   
    # 第3天同时吞没第1天
    if min(startPriceOfDay3,endPriceOfDay3) >= min(startPriceOfDay1,endPriceOfDay1):
      return False
    if max(startPriceOfDay3,endPriceOfDay3) <= max(startPriceOfDay1,endPriceOfDay1):
      return False

    return True

  # 日K线金针探底
  def isGoldenPinBottom(self,res,parseDay):
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

    # 下引线相对长度（按《日本蜡烛图技术》的定义，至少2倍）
    rate = downLine/entity
    if rate < 2:
      return False
    
    # 触及n日最低价（用于排除上吊线）
    if not self.isTouchMinPriceOfDays(res,parseDay,5):
      return False
    return True


  # 镊形底
  def isTweezersBottom(self,res,parseDay):
    dayList = self.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]  # 前一天
    day2 = dayList[1]  # 后一天
    
    # 前一天触及n日最低价
    if not self.isTouchMinPriceOfDays(res,day1,5):
      return False

    # 两天的最低价“接近或一致”
    minPriceOfDay1 = self.getMinPriceOfDay(res,day1)
    minPriceOfDay2 = self.getMinPriceOfDay(res,day2)
    rate = abs((minPriceOfDay2- minPriceOfDay1)/minPriceOfDay1)
    if rate > 0.005:  # 差距在0.5%以内
      return False

    return True

  def isUpGap(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]
    day2 = dayList[1]
    maxPriceOfDay1 = self.getMaxPriceOfDay(res,day1)
    minPriceOfDay2 = self.getMinPriceOfDay(res,day2)
    return minPriceOfDay2 > maxPriceOfDay1

  

  
  def haveTrends(self,kLines):
    # 收盘价
    if not (kLines[1]['end'] < kLines[7]['end']):
      return False
    if not (kLines[2]['end'] < kLines[8]['end']):
      return False
    
    # 最低价
    if not (kLines[1]['min'] < kLines[7]['min']):
      return False
    if not (kLines[2]['min'] < kLines[8]['min']):
      return False
    
    # 平均价
    if not (kLines[1]['avg'] < kLines[7]['avg']):
      return False
    if not (kLines[2]['avg'] < kLines[8]['avg']):
      return False


    # 预期价与当前价的比较：不能低于当前价
    if (kLines[7]['end'] + (kLines[7]['end'] - kLines[1]['end'])) < kLines[12]['end']:
      return False
    if (kLines[7]['min'] + (kLines[7]['min'] - kLines[1]['min'])) < kLines[12]['min']:
      return False
    if (kLines[7]['avg'] + (kLines[7]['avg'] - kLines[1]['avg'])) < kLines[12]['avg']:
      return False

    return True


  def haveSignals(self,res,parseDay,id):
    # 信号：缩量大秃阳线
    if self.isBigBaldRiseLineAndVolumeReduce(res,parseDay):
      print id,'缩量大秃阳线'
      return True
    
    # 信号：金针探底
    if self.isGoldenPinBottom(res,parseDay):
      print id,'金针探底'
      return True

    # 信号：镊形底
    if self.isTweezersBottom(res,parseDay):
      print id,'镊形底'
      return True

    # 信号：吞没线
    if self.isSwallowUp(res,parseDay):
      print id,'吞没线'
      return True

    # 信号：向上缺口
    if self.isUpGap(res,parseDay):
      print id,'向上缺口'
      return True

    return False


  # 解析
  # ================================================================================
  def parse(self,res,parseDay,id=''):
    # 趋势
    kLines = self.genKLines(res,parseDay)
    if not self.haveTrends(kLines):
      return False
    
    # 信号
    if not self.haveSignals(res,parseDay,id):
      return False

    return True



if __name__ == '__main__':
  print 'WJParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = WJParser(parseDay).getParseResult(True)
  print idList

















