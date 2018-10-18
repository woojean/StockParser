#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-17
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
 
reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
相对强度的涨停板
'''
class RelativeUpwardLimitParser(BaseParser):
  _tag = 'RelativeUpwardLimitParser'

  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 


  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    idFile = 'upward-limit-20160831-20180831/'+self._parseDay+'-RelativeUpwardLimitParser.sel'
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

    # 根据比较结果过滤
    # idList = self.calcuR(idList,1)

    if isDump:
      self.dumpIdList(idList)

    return idList


  # def getParseResult(self,isDump=False):
  #   idList = []
  #   num = 0
  #   parsedNum = 0
  #   priceFileList = BaseParser.getPriceFileList()
  #   total = len(priceFileList)
  #   for f in priceFileList:
  #     try:
  #       self.printProcess(parsedNum,total)
  #       id = f[-6:]
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

  #   # 根据比较结果过滤
  #   # idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)
  #   return idList


  # 振幅排名
  # def calcuR(self,idList,num):
  #   vList = []
  #   for id in idList:
  #     path = Tools.getPriceDirPath()+'/'+str(id)
  #     res = open(path,'r').read()
  #     minPrice = self.getMinPriceOfDay(res,self._parseDay)
  #     maxPrice = self.getMaxPriceOfDay(res,self._parseDay)
  #     a = maxPrice/minPrice
  #     vList.append((id,a))

  #   sList = sorted(vList,key=lambda x: x[1]) # 
  #   print "sorted list:"
  #   print sList
  #   selectedList = sList[:num]

  #   print "\nselected list:"
  #   print selectedList
  #   l = []
  #   for item in selectedList:
  #     l.append(item[0])
  #   return l


  # 均线距离
  def calcuR(self,idList,num):
    maDays = 10  # 均线
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      (v,v,ma) =  self.getMAPrice(res,self.getPastTradingDayList(self._parseDay,maDays))
      endPrice = self.getEndPriceOfDay(res,self._parseDay)
      if ma == -1 or endPrice ==0:
        continue
      r = endPrice/ma
      vList.append((id,r))

    # 排序
    sList = sorted(vList,key=lambda x: x[1]) # 
    print "sorted list:"
    print sList
    selectedList = sList[:num]

    print "\nselected list:"
    print selectedList
    l = []
    for item in selectedList:
      l.append(item[0])
    return l



  def isUpwardLimit(self,res,parseDay):
    dayList = self.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]
    day2 = dayList[1]
    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    if endPrice1 == 0 or endPrice2 ==0:
      return False

    # 排除一字板
    startPrice2 = self.getStartPriceOfDay(res,day2)
    minPrice2 = self.getMinPriceOfDay(res,day2)
    maxPrice2 = self.getMaxPriceOfDay(res,day2)
    if maxPrice2 == minPrice2 and startPrice2 == minPrice2:
      return False

    rate = (endPrice2 - endPrice1)/endPrice1
    if rate > 0.099:
      return True
    else:
      return False
    


  def parse(self,res,parseDay,id=''):
    
    isUpwardLimit = self.isUpwardLimit(res,parseDay)
    if not isUpwardLimit:
      return False

    # JKD多头排列且上涨
    # if not KdjParser.isKdjBull(parseDay,id):
    #   return False

    # 最高价低于5日线
    # (v,v,ma) =  self.getMAPrice(res,self.getPastTradingDayList(parseDay,5))
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # print maxPrice,ma
    # if maxPrice >= ma:
    #   return False

    # SLOWKD近期有死叉
    # if KdjParser.haveDeathCross(parseDay,id,5,5):
    #   return False

    # D低于20
    if not KdjParser.isDLow(parseDay,id):
      return False

    return True


if __name__ == '__main__':
  print 'RelativeUpwardLimitParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = RelativeUpwardLimitParser(parseDay).getParseResult(True)
  print idList

















