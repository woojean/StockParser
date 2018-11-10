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
  

  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    idFile = '555/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
    allIdList = Tools.getIdListOfFile(idFile)
    idList = []
    num = 0
    parsedNum = 0
    total = len(allIdList)
    for id in allIdList:
      try:
        self.printProcess(parsedNum,total)
        f = Tools.getPriceDirPath()+'/'+id
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
      # idList = self.calcuR(idList,1)

    if isDump:
      self.dumpIdList(idList)

    return idList


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
  
  def calcuR1(self,idList,num):
    maDays = 10  # 均线
    vList = []
    for id in idList:
      score = KdjParser.getD(parseDay,id)
      vList.append((id,score))

    # 排序
    sList = sorted(vList,key=lambda x: x[1]) 
    print "sorted list:"
    print sList
    selectedList = sList[:num]

    print "\nselected list:"
    print selectedList
    l = []
    for item in selectedList:
      l.append(item[0])
    return l



  def parse(self,res,parseDay,id=''):
    # 取参
    dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
    (v,v,ma) = self.getMAPrice(res,dayList)
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
    if ma < 0:
      return False

    ###############################################################

    # 阳线
    if endPrice <= startPrice:
      return False

    # 最高价位于ma之下
    if maxPrice >= ma:
      return False

    # 向上波幅 大于n%
    minP = min(endPriceOfLastDay,minPrice)  # 取昨日收盘价和今日最低价中的最小值
    r = (maxPrice - minP)/minP
    if (r < 0.05):
      return False


    # 排除SLOWKD近3日有死叉
    # if KdjParser.haveDeathCross(parseDay,id,4,5):
    #   return False


    # D低于20
    # if not KdjParser.isDLow(parseDay,id):
      # return False

    # 剔除ST
    # name = Tools.getNameById(id)
    # if 'ST' in name:
    #   return False

    # D底部反转
    # if not KdjParser.isDBottomReversal(parseDay,id):
      # return False

    # BIAS为负
    # if not BiasParser.isBiasNegative(parseDay,id):
      # return False

    # 前一日BIAS新低
    # if not BiasParser.isBiasMinOfDays(dayList[-2],20,id):
    #   return False


    return True



if __name__ == '__main__':
  print 'MaxPriceUnderMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaxPriceUnderMaParser(parseDay).getParseResult(True)
  print idList

















