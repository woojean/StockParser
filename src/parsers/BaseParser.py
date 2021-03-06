#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-08
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

class BaseParser:
  _parseDay = ''
  _tag = ''

  def __init__(self,parseDay): 
  	self._parseDay = parseDay
  
  # static
  # ----------------------------------------------------------------------------------------
  @staticmethod
  def getParseDay():
    day = time.strftime('%Y-%m-%d',time.localtime(time.time())) if (len(sys.argv) <= 1) else sys.argv[1]
    return day

  def parse(self,res,parseDay):
    pass

  @staticmethod
  def getPriceFileList():
    priceFilePath = Tools.getPriceDirPath()
    priceFileList = []
    for root,dirs,files in os.walk(priceFilePath):
      for f in files:
        try:
          if len(f) == 6:
            id = f
            path = root + '/' + id
            priceFileList.append(path)
        except Exception, e:
          pass
          #print repr(e)
    return priceFileList
    

  @staticmethod
  def getMacdFileList():
    macdFilePath = Tools.getMacdDirPath()
    macdFileList = []
    for root,dirs,files in os.walk(macdFilePath):
      for f in files:
        try:
          if len(f) == 6:
            id = f
            path = root + '/' + id
            macdFileList.append(path)
        except Exception, e:
          pass
          #print repr(e)
    return macdFileList
  
  @staticmethod
  def getKdjFileList():
    kdjFilePath = Tools.getKdjDirPath()
    kdjFileList = []
    for root,dirs,files in os.walk(kdjFilePath):
      for f in files:
        try:
          if len(f) == 6:
            id = f
            path = root + '/' + id
            kdjFileList.append(path)
        except Exception, e:
          pass
          #print repr(e)
    return kdjFileList

  @staticmethod
  def getKdjResOfId(id):
    kdjFileDir = Tools.getKdjDirPath()
    path = kdjFileDir + '/' +str(id)
    res = open(path,'r').read()
    return res


  @staticmethod
  def getBiasFileList():
    biasFilePath = Tools.getBiasDirPath()
    biasFileList = []
    for root,dirs,files in os.walk(biasFilePath):
      for f in files:
        try:
          if len(f) == 6:
            id = f
            path = root + '/' + id
            biasFileList.append(path)
        except Exception, e:
          pass
          #print repr(e)
    return biasFileList

  @staticmethod
  def getBiasResOfId(id):
    biasFileDir = Tools.getBiasDirPath()
    path = biasFileDir + '/' +str(id)
    res = open(path,'r').read()
    return res



  @staticmethod
  def getBasicInfoById(id):
    '''
    31 成交量
    36 量比
    
    37 换手率
    38 市盈率
    43 市净率
    
    45 流通市值
    46 总市值
    '''

    data = []
    try:
      path = Tools.getBasicDirPath()+'/'+str(id)
      res = open(path,'r').read()
      res = res[41:-1]
      data = eval(res)['Value']
    except Exception, e:
      pass
      #print repr(e)
    return data

  @staticmethod
  def getPastTradingDayList(lastDay,days):
    allDayList = Tools.getAllTradeDayList()
    idx = allDayList.index(lastDay)
    allDayList = allDayList[:idx+1]
    allDays = len(allDayList)
    return allDayList[allDays-days:]

  @staticmethod
  def getNextTradingDayList(firstDay,days):
    allDayList = Tools.getAllTradeDayList()
    idx = allDayList.index(firstDay)
    allDayList = allDayList[idx+1:]
    return allDayList[:days]


  # 获取某一日的增长率
  def getGrowthRate(self,id,startDay,endDay):
    try:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()

      startPrice = self.getEndPriceOfDay(res,startDay)
      endPrice = self.getEndPriceOfDay(res,endDay)

      rate = float((endPrice - startPrice)/startPrice)*100
    except Exception, e:
      rate = 0
      #print repr(e)
    return rate


  def isMaUpward(self,res,parseDay,maDays):
    dayList = self.getPastTradingDayList(parseDay,maDays+1)
    day1 = dayList[0]
    day2 = dayList[-1]
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0 :
      return False
    if endPrice2 <= endPrice1:
      return False
    return True
  





  # 判断是否处在上升趋势中（今日的ma60大于5天前的ma60）
  def isInRiseTrend(self,id,parseDay):
    try:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()

      dayList = self.getPastTradingDayList(parseDay,8)
      beginDay = dayList[0]
      endDay = dayList[-1]

      trendDay = 89

      (v,v,beginDayMa) = self.getMAPrice(res,self.getPastTradingDayList(beginDay,trendDay))
      (v,v,endDayMa) = self.getMAPrice(res,self.getPastTradingDayList(endDay,trendDay))

      isRise = (endDayMa > beginDayMa)
    except Exception, e:
      isRise = None
      #print repr(e)
    return isRise

  # 是否跌停
  def isDownwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPriceOfDay1 = self.getEndPriceOfDay(res,dayList[0])
    endPriceOfDay2 = self.getEndPriceOfDay(res,dayList[1])
    if 0 == endPriceOfDay1 or  0 == endPriceOfDay2:
      return False
    gr =  (endPriceOfDay2-endPriceOfDay1)/endPriceOfDay1
    if gr < -0.095:
      return True
    return False
 

  # 近期是否有跌停
  def recentlyHaveDownwardLimit(self,res,parseDay,days):
    haveDownwardLimit = False
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    for day in dayList:
      if self.isDownwardLimit(res,day):
        haveDownwardLimit = True
        break
    if not haveDownwardLimit:
      return False
    return True



  def isOneLineUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPriceOfDay1 = self.getEndPriceOfDay(res,dayList[0])
    endPriceOfDay2 = self.getEndPriceOfDay(res,dayList[1])
    if 0 == endPriceOfDay1 or  0 == endPriceOfDay2:
      return False

    # 一字板
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    if not minPrice == maxPrice:
      return False

    gr =  (endPriceOfDay2-endPriceOfDay1)/endPriceOfDay1
    if gr > 0.095:
      return True
    return False

  
  # 是否涨停
  def isUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPriceOfDay1 = self.getEndPriceOfDay(res,dayList[0])
    endPriceOfDay2 = self.getEndPriceOfDay(res,dayList[1])
    if 0 == endPriceOfDay1 or  0 == endPriceOfDay2:
      return False

    # 排除一字板
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    if minPrice == maxPrice:
      return False

    gr =  (endPriceOfDay2-endPriceOfDay1)/endPriceOfDay1
    if gr > 0.095:
      return True
    return False


  # 是否连板
  def isContinusUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    if not self.isUpwardLimit(res,dayList[0]):
      return False
    if not self.isUpwardLimit(res,dayList[1]):
      return False
    return True

  

  # 近期是否有连板
  def recentlyHaveContinusUpwardLimit(self,res,parseDay,days):
    have = False
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    for day in dayList:
      if self.isContinusUpwardLimit(res,day): # 排除一字板
        have = True
        break
    if not have:
      return False
    return True



  # 近期是否有涨停
  def recentlyHaveUpwardLimit(self,res,parseDay,days):
    haveUpwardLimit = False
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    for day in dayList:
      if self.isUpwardLimit(res,day): # 排除一字板
        haveUpwardLimit = True
        break
    if not haveUpwardLimit:
      return False
    return True
  

  # 近期是否有一字板涨停
  def recentlyHaveOneLineUpwardLimit(self,res,parseDay,days):
    haveUpwardLimit = False
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    for day in dayList:
      if self.isOneLineUpwardLimit(res,day): # 排除一字板
        haveUpwardLimit = True
        break
    if not haveUpwardLimit:
      return False
    return True
  

  # 过去指定天数涨停板数
  def countUpwardLimits(self,res,parseDay,days):
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    upwardLimitNum = 0
    for day in dayList:
      if self.isUpwardLimit(res,day):
        upwardLimitNum += 1
    return upwardLimitNum


  # 近阶段振幅
  def getAmplitudeOfDays(self,res,parseDay,days):
    minPrice = 99999
    maxPrice = 0
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    for day in dayList:
      minP = self.getMinPriceOfDay(res,day)
      maxP = self.getMaxPriceOfDay(res,day)
      if minP < minPrice:
        minPrice = minP
      if maxP > maxPrice:
        maxPrice = maxP
    if minPrice == 0:
      return False
    am = (maxPrice - minPrice)/minPrice
    return am



  # 均线穿越发生在3日内
  def isRecentlyPenetrate(self,id,parseDay):
    try:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()

      # 1 2 3 4
      dayList = self.getPastTradingDayList(parseDay,8)
      startDay = dayList[0]
      endDay = dayList[-1]

      shortTerm = 13
      longTerm = 34

      dayList = self.getPastTradingDayList(startDay,shortTerm)
      (v,v,startDayM13) = self.getMAPrice(res,dayList)
      dayList = self.getPastTradingDayList(startDay,longTerm)
      (v,v,startDayM34) = self.getMAPrice(res,dayList)

      dayList = self.getPastTradingDayList(endDay,shortTerm)
      (v,v,endDayM13) = self.getMAPrice(res,dayList)
      dayList = self.getPastTradingDayList(endDay,longTerm)
      (v,v,endDayM34) = self.getMAPrice(res,dayList)

      isRecentlyPenetrate = ((startDayM13 < startDayM34) and (endDayM13 > endDayM34))
    except Exception, e:
      isRecentlyPenetrate = None
      #print repr(e)
    return isRecentlyPenetrate


  def isMaInTrend(self,id,parseDay):
    try:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      dayList = self.getPastTradingDayList(parseDay,5)
      (v,v,ma5) = self.getMAPrice(res,dayList)
      dayList = self.getPastTradingDayList(parseDay,13)
      (v,v,ma13) = self.getMAPrice(res,dayList)
      dayList = self.getPastTradingDayList(parseDay,34)
      (v,v,ma34) = self.getMAPrice(res,dayList)

      isMaInTrend = True
      if ma5 < ma13:
        return False

      if ma13 < ma34:
        return False
    except Exception, e:
      isMaInTrend = None
      #print repr(e)
    return isMaInTrend
  

  def isInUpTrend(self,res,parseDay):
    if not self.isMaUpward(res,parseDay,5):
      return False
    if not self.isMaUpward(res,parseDay,10):
      return False
    if not self.isMaUpward(res,parseDay,20):
      return False

    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    (v,v,ma5) = self.getMAPrice(res,dayList)
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    (v,v,ma10) = self.getMAPrice(res,dayList)
    dayList = BaseParser.getPastTradingDayList(parseDay,20)
    (v,v,ma20) = self.getMAPrice(res,dayList)
    
    if not((ma5 > ma10) and (ma10 > ma20)):
      return False

    return True



  def isMaInUpTrend(self,res,parseDay,maDays1,maDays2):
    # 20日线向上
    # -------------------------------------------------------
    if not self.isMaUpward(res,parseDay,maDays1):
      return False

    # 60日线向上
    # -------------------------------------------------------
    if not self.isMaUpward(res,parseDay,maDays2):
      return False

    # 20日线在60日线上方
    # -------------------------------------------------------
    dayList = BaseParser.getPastTradingDayList(parseDay,maDays1)
    (v,v,ma20) = self.getMAPrice(res,dayList)
    dayList = BaseParser.getPastTradingDayList(parseDay,maDays2)
    (v,v,ma60) = self.getMAPrice(res,dayList)
    if ma20 < 0 or ma60<0:
      return False
    if not ma20 > ma60:
      return False

    return True


  def isMaUpwardReverse(self,res,parseDay,maDays):
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]
    day2 = dayList[1]
    day3 = dayList[2]
    dayList1 = BaseParser.getPastTradingDayList(day1,maDays)
    (v,v,ma1) = self.getMAPrice(res,dayList1)
    dayList2 = BaseParser.getPastTradingDayList(day2,maDays)
    (v,v,ma2) = self.getMAPrice(res,dayList2)
    dayList3 = BaseParser.getPastTradingDayList(day3,maDays)
    (v,v,ma3) = self.getMAPrice(res,dayList3)
    if not ((ma1 > ma2) and (ma3 > ma2)):
      return False
    return True


  
  def isVolumnShrink(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    v1 = self.getVolumeOfDay(res,lastDay)
    v2 = self.getVolumeOfDay(res,parseDay)
    if not v2 < v1:
      return False
    return True


  def getVolumnShrinkRate(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    v1 = self.getVolumeOfDay(res,lastDay)
    v2 = self.getVolumeOfDay(res,parseDay)
    if v1 == 0:
      return False
    rate = v2/v1
    return rate




  def isEndPriceUnderMa(self,res,parseDay,maDays):
    dayList = BaseParser.getPastTradingDayList(parseDay,maDays) 
    (v,v,ma) = self.getMAPrice(res,dayList)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if ma <0:
      return False
    if endPrice > ma:
      return False
    return True


  def isMaxPriceUnderMa(self,res,parseDay,maDays):
    dayList = BaseParser.getPastTradingDayList(parseDay,maDays) 
    (v,v,ma) = self.getMAPrice(res,dayList)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    if ma <0:
      return False
    if maxPrice > ma:
      return False
    return True


  def isMinPriceOnMa(self,res,parseDay,maDays):
    dayList = BaseParser.getPastTradingDayList(parseDay,maDays) 
    (v,v,ma) = self.getMAPrice(res,dayList)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    if ma <0:
      return False
    if ma > minPrice:
      return False
    return True
  

  def isMinPriceContinuousRise(self,res,parseDay,days,isJustRight = False):
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    ret = True
    for i in xrange(0,days-1):
      minPrice1 = self.getMinPriceOfDay(res,dayList[i])
      minPrice2 = self.getMinPriceOfDay(res,dayList[i+1])
      if (minPrice2 < minPrice1) or (0 == minPrice1*minPrice2):
        ret = False
        break

    if isJustRight:
      dayList = BaseParser.getPastTradingDayList(parseDay,days+1)
      minPrice1 = self.getMinPriceOfDay(res,dayList[0])
      minPrice2 = self.getMinPriceOfDay(res,dayList[1])
      if (minPrice1 < minPrice2) or (0 == minPrice1*minPrice2):
        ret = False

    return ret


  def isContinuouslySunny(self,res,parseDay,days,isJustRight = False):
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    ret = True
    for i in xrange(0,days):
      startPrice = self.getStartPriceOfDay(res,dayList[i])
      endPrice = self.getEndPriceOfDay(res,dayList[i])
      if (endPrice <= startPrice) or (0 == startPrice*endPrice):
        ret = False
        break

    if isJustRight:
      dayList = BaseParser.getPastTradingDayList(parseDay,days+1)
      startPrice = self.getStartPriceOfDay(res,dayList[0])
      endPrice = self.getEndPriceOfDay(res,dayList[0])
      if (endPrice >= startPrice) or (0 == startPrice*endPrice):
        ret = False

    return ret


  # compute
  # ----------------------------------------------------------------------------------------
  # def isInRiseTrend(self,res,day):
  #   dayListOf60 = self.getPastTradingDayList(day,60)
  #   dayListOf5 = self.getPastTradingDayList(day,5)
  #   ma60 = self.getMAPrice(res,dayListOf60)
  #   ma5 = self.getMAPrice(res,dayListOf5)
  #   return ma5 > ma60

  def isRise(self,res,day):
    startPrice = self.getStartPriceOfDay(res,day)
    endPrice = self.getEndPriceOfDay(res,day)
    return endPrice > startPrice

  # 涨幅
  def getRiseRate(self,res,day):
    rate = 0
    try:
      lastDay = self.getPastTradingDayList(day,2)[0]
      lastDayEndprice = self.getEndPriceOfDay(res,lastDay)
      endPrice = self.getEndPriceOfDay(res,day)
      rate = (endPrice - lastDayEndprice)/lastDayEndprice
    except Exception, e:
      #print repr(e)
      pass
    return rate


  '''
  0        1        2        3        4        5         6        7
  13.97,   14.20,   14.45,   13.73,   81722,   1.15亿,   5.14%    1.6
  开盘      收盘     最高      最低     成交量    成交额     振幅     换手率
  '''
  # 获取某一日的振幅
  def getAmplitudeOfDay(self,res,day):
    try:
      v = (re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[6]
      v = v.replace('%','')
      amplitude = float(v)/100.0
    except Exception, e:
      amplitude = 0
      #print repr(e)
    return amplitude

  # 获取某一日的换手率
  def getChangeRateOfDay(self,res,day):
    try:
      rate = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[7])/100.0
    except Exception, e:
      rate = 0
      #print repr(e)
    return rate


  # 获取某一日的成交额
  def getDealAmount(self,res,day):
    try:
      amount = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[5])
    except Exception, e:
      amount = 0
      #print repr(e)
    return amount



  # 获取某一日的开盘价
  def getStartPriceOfDay(self,res,day):
    try:
      price = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[0])
    except Exception, e:
      price = 0
      #print repr(e)
    return price


  # 获取某一日的收盘价
  def getEndPriceOfDay(self,res,day):
    try:
      price = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[1])
    except Exception, e:
      price = 0
    return price


  # 获取某一日的最低价
  def getMinPriceOfDay(self,res,day):
    try:
      price = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[3])
    except Exception, e:
      price = 0
    return price


  # 获取某一日的最高价
  def getMaxPriceOfDay(self,res,day):
    try:
      price = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[2])
    except Exception, e:
      price = 0
    return price

  # 获取某一日的成交量
  def getVolumeOfDay(self,res,day):
    try:
      volume = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[4])
    except Exception, e:
      volume = 0
    return volume

  # 获取平均成交量
  def getMaVolume(self,res,dayList):
    try:
      sumVolume = 0
      for d in dayList:
        v = self.getVolumeOfDay(res,d)
        sumVolume += v
      maVolume = sumVolume/len(dayList)
    except Exception, e:
      maVolume = 0
    return maVolume


  # 量在均量线下
  def isVolumnUnderMv(self,res,parseDay,days):
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    maVolume = self.getMaVolume(res,dayList)
    volumn = self.getVolumeOfDay(res,parseDay)
    if volumn < maVolume:
      return True
    return False



  # 获取量比
  def getVolumeRatioOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    parseDayVolume = self.getVolumeOfDay(res,day)

    sumVolume = 0
    for d in dayList:
      volume = self.getVolumeOfDay(res,d)
      sumVolume += volume
    maVolume = sumVolume/days
    ratio = parseDayVolume/maVolume

    return ratio


  # 是否阳线
  def isYangXian(self,res,day):
    startPrice = self.getStartPriceOfDay(res,day)
    endPrice = self.getEndPriceOfDay(res,day)
    if startPrice ==0 or endPrice ==0:
      return False
    if endPrice <= startPrice:
      return False
    return True

  
  # 是否向上跳空缺口
  def isUpwardGap(self,res,parseDay):
    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    maxPrice1 = self.getMaxPriceOfDay(res,lastDay)
    minPrice2 = self.getMinPriceOfDay(res,parseDay)
    if 0 == maxPrice1*minPrice2:
      return False

    if not(minPrice2 - maxPrice1 > 0.01):
      return False

    return True


  # 获取振幅
  def getAm(self,res,day):
    minPrice = self.getMinPriceOfDay(res,day)
    maxPrice = self.getMaxPriceOfDay(res,day)
    if minPrice ==0 or maxPrice ==0:
      return False
    am = (maxPrice - minPrice)/minPrice
    return am


  # 获取实体振幅
  def getEntityAm(self,res,day):
    startPrice = self.getStartPriceOfDay(res,day)
    endPrice = self.getEndPriceOfDay(res,day)
    minPrice = min(startPrice,endPrice)
    maxPrice = max(startPrice,endPrice)
    if minPrice ==0 or maxPrice ==0:
      return False
    am = (maxPrice - minPrice)/minPrice
    return am


  # 判断某一天是否是过去若干天的最大成交量
  def isMaxVolumeOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    maxVolume = self.getVolumeOfDay(res,day)

    otherDayMaxVolume = 0
    for d in dayList:
      volume = self.getVolumeOfDay(res,d)
      if volume > otherDayMaxVolume: # 错误数据（交易日不连贯）
        otherDayMaxVolume = volume
    return maxVolume > otherDayMaxVolume


  # 判断某一天是否是过去若干天的最小成交量
  def isMinVolumeOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    minVolume = self.getVolumeOfDay(res,day)

    otherDayMinVolume = 99999999999
    for d in dayList:
      volume = self.getVolumeOfDay(res,d)
      if volume < otherDayMinVolume: # 错误数据（交易日不连贯）
        otherDayMinVolume = volume
    return minVolume < otherDayMinVolume


  # 获取某一日的振幅
  def getAmplitude(self,res,day):
    lastDay = BaseParser.getPastTradingDayList(day,2)[0]
    lastDayEndPrice = self.getEndPriceOfDay(res,lastDay)
    minPrice = self.getMinPriceOfDay(res,day)
    maxPrice = self.getMaxPriceOfDay(res,day)
    amplitude = (maxPrice - minPrice)/lastDayEndPrice
    return amplitude


  # 判断某一天是否是过去若干天的最低价
  def isTouchMinPriceOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    minPrice = self.getMinPriceOfDay(res,day)

    otherDayMinPrice = 9999999.0
    for d in dayList:
      price = self.getMinPriceOfDay(res,d)
      if price < otherDayMinPrice: # 错误数据（交易日不连贯）
        otherDayMinPrice = price
    return minPrice <= otherDayMinPrice


  # 获取时间区间最低价
  def getMinPriceOfDays(self,res,dayList):
    minPrice = self.getMinPriceOfDay(res,dayList[0])
    for d in dayList:
      price = self.getMinPriceOfDay(res,d)
      if price < minPrice: # 错误数据（交易日不连贯）
        minPrice = price
    return minPrice

  # 获取时间区间最高价
  def getMaxPriceOfDays(self,res,dayList):
    maxPrice = self.getMaxPriceOfDay(res,dayList[0])
    for d in dayList:
      price = self.getMaxPriceOfDay(res,d)
      if price > maxPrice: # 错误数据（交易日不连贯）
        maxPrice = price
    return maxPrice



  # 判断某一天收盘价是否是过去若干天的最高价
  def isMaxPriceOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    maxPrice = self.getEndPriceOfDay(res,day)

    otherDayMaxPrice = 0
    for d in dayList:
      price = self.getMaxPriceOfDay(res,d)
      if price > otherDayMaxPrice: # 错误数据（交易日不连贯）
        otherDayMaxPrice = price
    return maxPrice > otherDayMaxPrice



  # 判断某一天的最低价是否为一段区间的最低价
  def haveMinPriceOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    minPrice = self.getMinPriceOfDay(res,day)

    otherDayMinPrice = 10000000
    for d in dayList:
      # price = self.getEndPriceOfDay(res,d)
      price = self.getMinPriceOfDay(res,d)
      if price < otherDayMinPrice: 
        otherDayMinPrice = price
    # print minPrice,otherDayMinPrice
    return minPrice < otherDayMinPrice

  
  def intervalMinPriceOfDays(self,res,parseDay,days1,days2):
    minPriceOfInterval = 100000
    dayList = BaseParser.getPastTradingDayList(parseDay,days1)
    for d in dayList:
      price = self.getMinPriceOfDay(res,d)
      if price < minPriceOfInterval: 
        minPriceOfInterval = price

    dayList = BaseParser.getPastTradingDayList(parseDay,days2)
    otherDayMinPrice = 10000000
    for d in dayList:
      # price = self.getEndPriceOfDay(res,d)
      price = self.getMinPriceOfDay(res,d)
      if price < otherDayMinPrice: 
        otherDayMinPrice = price
    # print minPrice,otherDayMinPrice
    return minPriceOfInterval <= otherDayMinPrice


  '''
  dayList = getComputeDayList(day,5)
  (v1,v2,ma5) = computeMAPrice(res,dayList)
  '''
  def getMAPrice(self,res,dayList):
    days = len(dayList)
    sumPrice = 0.0
    for day in dayList:
      price = self.getEndPriceOfDay(res,day)
      if price == 0: # 错误数据（交易日不连贯）
        sumPrice = -1
        break  # 非周末的节假日
      sumPrice += price
    maPrice = sumPrice / days
    lastDayStartPrice = self.getStartPriceOfDay(res,dayList[-1])
    lastDayEndPrice = self.getEndPriceOfDay(res,dayList[-1])
    return (lastDayStartPrice,lastDayEndPrice,maPrice)


  def getMv(self,res,dayList):
    days = len(dayList)
    sumV = 0.0
    for day in dayList:
      v = self.getVolumeOfDay(res,day)
      if v == 0: # 错误数据（交易日不连贯）
        sumV = -1
        break  # 非周末的节假日
      sumV += v
    mv = sumV / days
    return mv


  def isNewStock(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2) 
    lastDay = dayList[-2]
    v = self.getVolumeOfDay(res,lastDay)
    if v <= 0 :
      return True
    return False

  

  def isMinPriceUpwardReverse(self,res,parseDay):
    dayList = self.getPastTradingDayList(parseDay,3)
    min1 = self.getMinPriceOfDay(res,dayList[0])
    min2 = self.getMinPriceOfDay(res,dayList[1])
    min3 = self.getMinPriceOfDay(res,dayList[2])
    
    if min1==0 or min2 ==0 or min3 ==0:
      return False
    
    if not ((min1 > min2) and (min3 > min2)):
      return False
    
    return True


  def isRgb(self,res,parseDay):
    R = 5
    G = 10
    B = 20
      
    dayList = self.getPastTradingDayList(parseDay,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(parseDay,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(parseDay,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if not ((maR > maG) and (maG > maB)):
      return False

    return True

  
  def isMaUpwardReverse(self,res,parseDay,maDays):
    dayList = self.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]
    day2 = dayList[1]
    day3 = dayList[2]

    dayList1 = self.getPastTradingDayList(day1,maDays)
    (v,v,ma1) = self.getMAPrice(res,dayList1)

    dayList2 = self.getPastTradingDayList(day2,maDays)
    (v,v,ma2) = self.getMAPrice(res,dayList2)

    dayList3 = self.getPastTradingDayList(day3,maDays)
    (v,v,ma3) = self.getMAPrice(res,dayList3)

    if not ((ma1 > ma2) and (ma3 > ma2)):
      return False

    return True



  # 缩量（相对前一日）
  def isVolumnDecline(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    v1 = self.getVolumeOfDay(res,lastDay)
    v2 = self.getVolumeOfDay(res,parseDay)
    if not v2 < v1:
      return False
    return True


  # 近n日涨幅
  def getGrOfDays(self,res,parseDay,days):
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    endPrice1 = self.getEndPriceOfDay(res,dayList[0])
    endPrice2 = self.getEndPriceOfDay(res,parseDay)
    if endPrice1 == 0:
      return False

    gr = (endPrice2 - endPrice1)/endPrice1
    return gr
  
  # 量是n日最低
  def minVolumnOfDays(self,res,parseDay):
    days = 0
    volume = self.getVolumeOfDay(res,parseDay)
    if volume <=0 :
      return 0
    dayList = self.getPastTradingDayList(parseDay,100)
    dayList.reverse()
    for day in dayList:
      days += 1
      v = self.getVolumeOfDay(res,day)
      if (v < volume) and ( v > 0 ):
        break
    return days
  

  # 量是n日最大
  def maxVolumnOfDays(self,res,parseDay):
    days = 0
    volume = self.getVolumeOfDay(res,parseDay)
    if volume <=0 :
      return 0
    dayList = self.getPastTradingDayList(parseDay,100)
    dayList.reverse()
    for day in dayList:
      days += 1
      v = self.getVolumeOfDay(res,day)
      if (v > volume) and ( v > 0 ):
        break
    return days


  #  inherit
  # ----------------------------------------------------------------------------------------
  def dumpIdList(self,idList):
    print 'dumpIdList'
    enterListDirPath = Tools.getEnterListDirPath()
    #open('data/golden-pin-bottom/'+ confirmDay +'.sel','w').write(','.join(idList))
    open(enterListDirPath + '/' + self._parseDay + '-'+ self._tag+'.sel','w').write(','.join(idList))
    print "\n\n",self._parseDay
    print "============================================ Result ============================================ \n"
    print str(idList) + "\n\n"
    print " - " + str(len(idList)) + " - \n\n"

  def printProcess(self,current,total):
    lastRate = round((current-1)*100.0/total,0)
    currentRate = round(current*100.0/total,0)
    if lastRate != currentRate:
      rate = str(int(currentRate)) 
      rate = rate.rjust(3,' ')
      s = ''
      s = s.rjust(int(currentRate),'.')
      s += ' -> '
      s = s.ljust(104,' ')
      s += rate + ' %'
      print s

  
  def calcuR(self,idList,num):
    return idList
  


  def getParseResult(self,isDump=False):
    idList = []
    num = 0
    parsedNum = 0
    priceFileList = BaseParser.getPriceFileList()
    total = len(priceFileList)
    for f in priceFileList:
      try:
        self.printProcess(parsedNum,total)
        id = f[-6:]
        res = open(f,'r').read()
        ret = self.parse(res,self._parseDay,id)
        if ret:
          idList.append(id)
          num += 1
          print str(num) + ' ↗'
        parsedNum += 1
      except Exception, e:
        pass
        print repr(e)

    # 根据打分结果过滤
    idList = self.calcuR(idList,10)

    if isDump:
      self.dumpIdList(idList)

    return idList


  # def getParseResult(self,isDump=False):
  #   print '***************************************************************************'
  #   print 'In custom mode'
  #   print '***************************************************************************'
  #   idFile = '555/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
  #   allIdList = Tools.getIdListOfFile(idFile)
  #   idList = []
  #   num = 0
  #   parsedNum = 0
  #   total = len(allIdList)
  #   for id in allIdList:
  #     try:
  #       self.printProcess(parsedNum,total)
  #       f = Tools.getPriceDirPath()+'/'+id
  #       res = open(f,'r').read()
  #       ret = self.parse(res,self._parseDay,id)
  #       if ret:
  #         idList.append(id)
  #         num += 1
  #         print str(num) + ' ↗'
  #       parsedNum += 1
  #     except Exception, e:
  #       pass
  #       print repr(e)
        
  #     # 根据打分结果过滤
  #     idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList







