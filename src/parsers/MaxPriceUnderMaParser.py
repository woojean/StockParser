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
from KdjParser import KdjParser
from BiasParser import BiasParser
from common import Tools
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
最高价低于5日线的大阳线
'''
class MaxPriceUnderMaParser(BaseParser):
  _tag = 'MaxPriceUnderMaParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

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
      
  #   print idList

  #   # 根据打分结果过滤
  #   # idList = self.calcuR(idList,3)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList


  def isMaxPriceUnderMa(self,res,day,days):
    maxPrice = self.getMaxPriceOfDay(res,day)
    dayList = BaseParser.getPastTradingDayList(day,days)
    (v,v,ma) = self.getMAPrice(res,dayList)
    if maxPrice < ma:
      return True
    return False


  def isUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPrice1 = self.getEndPriceOfDay(res,dayList[-2])
    endPrice2 = self.getEndPriceOfDay(res,dayList[-1])
    if endPrice1 == 0 or  endPrice2 == 0:
      return False
    r = (endPrice2 - endPrice1)/endPrice1
    if r < 0.09:
      return False
    return True

  def isDownwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPrice1 = self.getEndPriceOfDay(res,dayList[-2])
    endPrice2 = self.getEndPriceOfDay(res,dayList[-1])
    if endPrice1 == 0 or  endPrice2 == 0:
      return False
    r = (endPrice2 - endPrice1)/endPrice1
    if r > -0.09:
      return False
    return True


  def isDownwardGap(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    minPrice1 = self.getMinPriceOfDay(res,dayList[-2])
    maxPrice2 = self.getMaxPriceOfDay(res,dayList[-1])
    if minPrice1 == 0 or  maxPrice2 == 0:
      return False
    if maxPrice2 >= minPrice1:
      return False
    return True


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


  def isLongUpLine(self,res,parseDay):
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    totalLine = maxPrice - minPrice
    upLine = maxPrice - max(startPrice,endPrice)
    if totalLine == 0 :
      return True
    r = upLine/totalLine
    if r > 0.33:
      return True
    return False


  def isLongDownLine(self,res,parseDay):
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    totalLine = maxPrice - minPrice
    downLine = min(startPrice,endPrice) - minPrice
    if totalLine == 0 :
      return False
    r = downLine/totalLine
    if r < 0.5:
      return False
    return True



  # def calcuR(self,idList,num):
  #   vList = []
  #   for id in idList:
  #     path = Tools.getPriceDirPath()+'/'+str(id)
  #     res = open(path,'r').read()

  #     # 振幅
  #     minPrice = self.getMinPriceOfDay(res,parseDay)
  #     maxPrice = self.getMaxPriceOfDay(res,parseDay)
  #     minP = minPrice
  #     score = (maxPrice - minP)/minP

  #     # 换手率
  #     # score = self.getChangeRateOfDay(res,parseDay)

  #     # 5日量比
  #     # dayList = BaseParser.getPastTradingDayList(parseDay,5)
  #     # mv5 = self.getMv(res,dayList)
  #     # v = self.getVolumeOfDay(res,parseDay)
  #     # score = v/mv5

  #     # 市值最小
  #     # cr = self.getChangeRateOfDay(res,parseDay)
  #     # amout = self.getDealAmount(res,parseDay)
  #     # marketValue = amout/cr
  #     # marketValue = marketValue/100000000.0
  #     # score = marketValue


  #     vList.append((id,score))

  #   # 排序
  #   sList = sorted(vList,key=lambda x: -x[1]) 
  #   print "sorted list:"
  #   print sList
  #   selectedList = sList[:num]

  #   print "\nselected list:"
  #   print selectedList
  #   l = []
  #   for item in selectedList:
  #     l.append(item[0])
  #   return l



  def parse(self,res,parseDay,id=''):
    # 取参
    dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
    lastDay = dayList[-2]
    # (v,v,ma5) = self.getMAPrice(res,dayList)
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    startPriceOfLastDay = self.getStartPriceOfDay(res,dayList[-2])
    endPriceOfLastDay = self.getEndPriceOfDay(res,dayList[-2])
    minPriceOfLastDay = self.getMinPriceOfDay(res,dayList[-2])
    maxPriceOfLastDay = self.getMaxPriceOfDay(res,dayList[-2])

    # 参数校验
    if startPrice ==0 or endPrice ==0 or minPrice ==0 or maxPrice ==0:
      return False
    # if ma5 < 0:
    #   return False

    ###############################################################

    # 阳线
    if endPrice <= startPrice:
      return False

    # 最高价位于ma之下
    # if maxPrice >= ma5:
    #   return False

    # 量在5日均量线上
    # mv5 = self.getMv(res,dayList)
    # if mv5 == -1:
    #   return False
    # v = self.getVolumeOfDay(res,parseDay)
    # if v < mv5:
    #   return False


    
    # 近3日有向下跳空缺口
    # cDayList = BaseParser.getPastTradingDayList(parseDay,3)
    # haveDownwardGap = False
    # for day in cDayList:
    #   if self.isDownwardGap(res,day):
    #     haveDownwardGap = True
    #     break
    # if not haveDownwardGap:
    #   return False


    # 不搭在60日线上
    # onMa60 = False
    # onMa250 = False
    # maDayList = BaseParser.getPastTradingDayList(parseDay,60) 
    # (v,v,ma60) = self.getMAPrice(res,maDayList)
    # if (minPrice <= ma60) and (maxPrice >= ma60):
    #   onMa60 = True
    

    # # 不搭在250日线上
    # maDayList = BaseParser.getPastTradingDayList(parseDay,250) 
    # (v,v,ma250) = self.getMAPrice(res,maDayList)
    # if (minPrice <= ma250) and (maxPrice >= ma250):
    #   onMa250 = True

    # if (not onMa60) and (not onMa250):
    #   return False


    # 大长腿
    # if not self.isLongDownLine(res,parseDay):
      # return False


    # 光头
    # if endPrice < maxPrice:
      # return False

    # 量为n日最高
    # if not self.isMaxVolumeOfDays(res,parseDay,5):
    #   return False

    # 量为n日最低
    # if not self.isMinVolumeOfDays(res,parseDay,5):
    #  return False
   

    # 振幅大于n%
    minP = minPrice
    r = (maxPrice - minP)/minP
    if (r < 0.07):
      return False


    # 向上波幅 大于n%
    # minP = min(endPriceOfLastDay,minPrice)  # 取昨日收盘价和今日最低价中的最小值
    # r = (maxPrice - minP)/minP
    # if (r < 0.05):
    #   return False


    # 排除SLOWKD近3日有死叉
    # if KdjParser.haveDeathCross(parseDay,id,4,5):
    #   return False

    # 流通值小于100亿
    # cr = self.getChangeRateOfDay(res,parseDay)
    # amout = self.getDealAmount(res,parseDay)
    # marketValue = amout/cr
    # marketValue = marketValue/100000000.0
    # # print id,marketValue
    # if marketValue>100.0:
    #   print 'Tooooooo big'
    #   return False

    # D低于20
    # if not KdjParser.isDLow(parseDay,id):
    #   return False

    # 剔除ST
    # name = Tools.getNameById(id)
    # if 'ST' in name:
    #   return False

    # D底部反转
    # if not KdjParser.isDBottomReversal(parseDay,id):
    #   return False

    # BIAS为负
    # if not BiasParser.isBiasNegative(parseDay,id):
      # return False

    # 前一日BIAS新低
    # if not BiasParser.isBiasMinOfDays(dayList[-2],20,id):
      # return False

    
    #######################################################################
    # 昨日是5日线下阳线
    # startPriceOfLastDay = self.getStartPriceOfDay(res,lastDay)
    # endPriceOfLastDay = self.getEndPriceOfDay(res,lastDay)
    # minPriceOfLastDay = self.getMinPriceOfDay(res,lastDay)
    # maxPriceOfLastDay = self.getMaxPriceOfDay(res,lastDay)
    # if endPriceOfLastDay <= startPriceOfLastDay:
    #   return False
    # dayListOfLastDay = BaseParser.getPastTradingDayList(lastDay,5) 
    # (v,v,maOfLastDay) = self.getMAPrice(res,dayListOfLastDay)
    # if maxPriceOfLastDay >= maOfLastDay:
    #   return False

    # # 当日阴线
    # if endPrice >= startPrice:
    #   return False

    return True



if __name__ == '__main__':
  print 'MaxPriceUnderMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaxPriceUnderMaParser(parseDay).getParseResult(True)
  print idList

















