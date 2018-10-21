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
相对解析
'''
class RelativeParser(BaseParser):
  _tag = 'RelativeParser'

  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 


  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    idFile = 'yx/'+self._parseDay+'-RelativeParser.sel'
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
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      # 实体最大
      # startPrice = self.getStartPriceOfDay(res,self._parseDay)
      # if startPrice == 0:
      #   return False
      # endPrice = self.getEndPriceOfDay(res,self._parseDay)
      # r = endPrice/startPrice
      
      # 振幅最大
      # minPrice = self.getMinPriceOfDay(res,self._parseDay)
      # if minPrice == 0:
      #   return False
      # maxPrice = self.getMaxPriceOfDay(res,self._parseDay)
      # r = maxPrice/minPrice

      # 距离5日线最远
      # dayList = BaseParser.getPastTradingDayList(self._parseDay,5)
      # (v,v,ma) = self.getMAPrice(res,dayList)
      # maxPrice = self.getMaxPriceOfDay(res,self._parseDay)
      # r = ma/maxPrice

      # 涨幅最大
      # dayList = BaseParser.getPastTradingDayList(self._parseDay,2)
      # endPrice1 = self.getEndPriceOfDay(res,dayList[0])
      # endPrice = self.getEndPriceOfDay(res,self._parseDay)
      # if endPrice1 == 0:
      #   return False
      # r = endPrice/endPrice1

      # 近10日跌幅最大
      dayList = BaseParser.getPastTradingDayList(self._parseDay,10)
      startDay = dayList[0]
      endPrice = self.getEndPriceOfDay(res,self._parseDay)
      endPriceS = self.getEndPriceOfDay(res,startDay)
      r = (endPrice - endPriceS)/endPriceS

      vList.append((id,r))

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


  def parse2(self,res,parseDay,id=''):
    # 取参
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    startDay = dayList[0]
    day1 = dayList[-2]
    endPriceS = self.getEndPriceOfDay(res,startDay)

    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)

    startPrice1 = self.getStartPriceOfDay(res,day1)
    endPrice1 = self.getEndPriceOfDay(res,day1)

    # endPriceOfLastDay = self.getEndPriceOfDay(res,dayList[-2])
    if startPrice ==0 or endPrice == 0 or minPrice == 0 or maxPrice == 0:
      return False
    
    if endPriceS == 0 or startPrice1 == 0 or endPrice1 == 0:
      return False
    

    # 近10日跌幅超过20%
    # dr = (endPrice - endPriceS)/endPriceS
    # if dr > -0.1:
    #   # print 'dr > -0.2'
    #   return False

    # 前一日非阳线
    if endPrice1 > startPrice1:
      # print 'endPrice1 > startPrice1'
      return False

    # 当日阳线
    if endPrice <= startPrice:
      # print 'endPrice <= startPrice'
      return False

    # 振幅大于7%
    ar = (maxPrice - minPrice)/minPrice
    if ar < 0.07:
      # print 'ar < 0.07'
      return False

    return True




  def parse(self,res,parseDay,id=''):
    # 取参
    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    (v,v,ma) = self.getMAPrice(res,dayList)
    if ma == -1:
      return False
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # endPriceOfLastDay = self.getEndPriceOfDay(res,dayList[-2])
    if startPrice ==0 or endPrice == 0 or minPrice == 0 or maxPrice == 0:
      return False


    # 阳线
    if endPrice <= startPrice:
      return False

    # 位于ma之下 = 最高价低于ma
    if maxPrice >= ma:
      return False

    # 相对前一日放量
    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0] # 前一日
    vOfParseDay = self.getVolumeOfDay(res,parseDay)
    vOfLastDay = self.getVolumeOfDay(res,lastDay)
    if 0 == vOfLastDay: # 前一日无量的排除，可能是未开板次新
      return False

    if vOfParseDay <= vOfLastDay: # 放量
      return False



    # 振幅大于7%
    # ar = (maxPrice - minPrice)/minPrice
    # if ar < 0.07:
    #   return False

    # 秃底
    # if not startPrice == minPrice:
    #   return False

    # 秃顶
    # if not endPrice == maxPrice:
    #   return False

    # SLOWKD近期有死叉
    # if KdjParser.haveDeathCross(parseDay,id,5,5):
    #   return False

    # D低于20
    # if not KdjParser.dIsLow(parseDay,id):
      # return False

    return True


if __name__ == '__main__':
  print 'RelativeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = RelativeParser(parseDay).getParseResult(True)
  print idList

















