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
WJ
'''
class WJParser(BaseParser):
  _tag = 'WJParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  # 趋势判断
  # ============================================================
  def isInRise(self,l):
    ret = True
    length = len(l)
    for i in xrange(0,length-1):
      if l[i] <0 or l[i+1]<0:
        ret = False
        break
      if l[i] >= l[i+1]: # MA = -1
        ret = False
        break
    return ret


  def isRiseIsStronger(self,res,parseDay):
    # 240-180 | 180-120 | 120-60 | 区间均价递增

    dayList = BaseParser.getPastTradingDayList(parseDay,240)
    dayList1 = dayList[0:60]
    dayList2 = dayList[60:120]
    dayList3 = dayList[120:180]
    dayList4 = dayList[180:240]
    
    (v,v,ma1) = self.getMAPrice(res,dayList1)
    (v,v,ma2) = self.getMAPrice(res,dayList2)
    (v,v,ma3) = self.getMAPrice(res,dayList3)
    (v,v,ma4) = self.getMAPrice(res,dayList4)
    
    if ma1<=0 or ma2<=0 or ma3<=0 or ma4<=0: # -1
      return False

    #print ma1,ma2,ma3,ma4

    if self.isInRise([ma2,ma3,ma4]):
      #print '〇↗↗↗'
      return True
    
    
    if self.isInRise([ma1,ma3,ma4]):
      #print '↗〇↗↗'
      return True

    
    if self.isInRise([ma1,ma2,ma4]):
      #print '↗↗〇↗'
      return True

    
    #if self.isInRise([ma1,ma2,ma3]):
    #  print '↗↗↗〇'
    #  return True

    return False



  # 光头光脚大阳线，且缩量
  # ============================================================
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

  
  # 收盘价向上穿透MA60
  # ============================================================
  def isPenetrateUpwardMa60(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]
    day2 = dayList[1]

    # 前一日收盘价在MA之下
    dayList = BaseParser.getPastTradingDayList(day1,60)
    (v,v,ma) = self.getMAPrice(res,dayList)
    endPrice1 = self.getEndPriceOfDay(res,day1)
    if endPrice1 >= ma:
      return False

    # 当日收盘价在MA之上
    dayList = BaseParser.getPastTradingDayList(day2,60)
    (v,v,ma) = self.getMAPrice(res,dayList)
    parseDayMa = ma
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice2 <= ma:
      return False

    return True


  # 均线形成三角托
  # ============================================================
  def isTriangularSupport(self,res,parseDay):
    dayList5 = BaseParser.getPastTradingDayList(parseDay,5)
    dayList10 = BaseParser.getPastTradingDayList(parseDay,10)
    dayList20 = BaseParser.getPastTradingDayList(parseDay,20)

    (v1,v2,ma5) = self.getMAPrice(res,dayList5)
    (v1,v2,ma10) = self.getMAPrice(res,dayList10)
    (v1,v2,ma20) = self.getMAPrice(res,dayList20)
    
    # 当日 ma5 > ma20 > ma10
    if not ((ma5 > ma20) and (ma20 > ma10)):
      return False

    if abs(ma20-ma5) < abs(ma20-ma10):
      return False

    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    parseDay = dayList[0]
    dayList5 = BaseParser.getPastTradingDayList(parseDay,5)
    dayList10 = BaseParser.getPastTradingDayList(parseDay,10)
    dayList20 = BaseParser.getPastTradingDayList(parseDay,20)
    (v1,v2,ma5) = self.getMAPrice(res,dayList5)
    (v1,v2,ma10) = self.getMAPrice(res,dayList10)
    (v1,v2,ma20) = self.getMAPrice(res,dayList20)

    # 2日前 ma20 > ma5 > ma10
    if not ((ma20 > ma5) and (ma5 > ma10)):
      return False

    return True


  # 日K线金针探底
  # ============================================================
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
    
    # 触及10日最低价（用于排除上吊线）
    if not self.isTouchMinPriceOfDays(res,parseDay,10):
      return False
    return True

  # 镊形底
  # ============================================================
  def isGoldenPinBottom(self,res,parseDay):
    ret = False
    
    dayList = self.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]  # 前一天
    day2 = dayList[1]  # 后一天
    
    # 前一天触及10日最低价
    if not self.isTouchMinPriceOfDays(res,day1,10):
      return False

    # 两天的最低价“接近或一致”
    minPriceOfDay1 = self.getMinPriceOfDay(res,day1)
    minPriceOfDay2 = self.getMinPriceOfDay(res,day2)
    rate = abs((minPriceOfDay2- minPriceOfDay1)/minPriceOfDay1)
    if rate > 0.001:
      return False

    return True


  def isTweezersBottom(self,res,parseDay):
    ret = False
    
    dayList = self.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]  # 前一天
    day2 = dayList[1]  # 后一天
    
    # 前一天触及10日最低价
    if not self.isTouchMinPriceOfDays(res,day1,10):
      return False

    # 两天的最低价“接近或一致”
    minPriceOfDay1 = self.getMinPriceOfDay(res,day1)
    minPriceOfDay2 = self.getMinPriceOfDay(res,day2)
    rate = abs((minPriceOfDay2- minPriceOfDay1)/minPriceOfDay1)
    if rate > 0.001:
      return False

    return True


  # 解析
  # ================================================================================
  def parse(self,res,parseDay,id=''):

    # 上升趋势
    if not self.isRiseIsStronger(res,parseDay):
      return False

    # 大秃阳线 + 缩量
    if self.isBigBaldRiseLineAndVolumeReduce(res,parseDay):
      return True

    # 上穿MA60
    if self.isPenetrateUpwardMa60(res,parseDay):
      return True

    # 均线三角托
    if self.isTriangularSupport(res,parseDay):
      return True

    # 金针探底
    if self.isGoldenPinBottom(res,parseDay):
      return True

    # 镊形底
    if self.isTweezersBottom(res,parseDay):
      return True

    return False



if __name__ == '__main__':
  print 'WJParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = WJParser(parseDay).getParseResult(True)
  print idList

















