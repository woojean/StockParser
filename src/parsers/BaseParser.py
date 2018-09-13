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
  def geChangeRateOfDay(self,res,day):
    try:
      rate = float((re.findall('"'+ day +',(.*?)"', res)[0]).split(',')[7])/100.0
    except Exception, e:
      rate = 0
      #print repr(e)
    return rate

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



  # 判断某一天是否是过去若干天的最高价
  def isMaxPriceOfDays(self,res,day,days):
    dayList = BaseParser.getPastTradingDayList(day,days)
    dayList = dayList[:-1]
    maxPrice = self.getEndPriceOfDay(res,day)

    otherDayMaxPrice = 0
    for d in dayList:
      price = self.getEndPriceOfDay(res,d)
      if price > otherDayMaxPrice: # 错误数据（交易日不连贯）
        otherDayMaxPrice = price
    return maxPrice > otherDayMaxPrice



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

  
  def isRgb(self,id,parseDay):
    path = Tools.getPriceDirPath()+'/'+str(id)
    res = open(path,'r').read()

    R = 5
    G = 8
    B = 13
      
    dayList = self.getPastTradingDayList(parseDay,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(parseDay,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(parseDay,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if not ((maR > maG) and (maG > maB)):
      return False

    return True

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

    if isDump:
      self.dumpIdList(idList)

    return idList

