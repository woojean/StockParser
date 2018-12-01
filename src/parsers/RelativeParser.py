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
from BiasParser import BiasParser
 
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


  # def getParseResult(self,isDump=False):
  #   print '***************************************************************************'
  #   print 'In custom mode'
  #   print '***************************************************************************'
  #   idFile = '实体振幅>5%的阳线/'+self._parseDay+'-RelativeParser.sel'
  #   # idFile = '5/'+self._parseDay+'-RelativeParser.sel'
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
  #   idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList


  # def calcuR(self,idList,num):
  #   vList = []
  #   for id in idList:
  #     path = Tools.getPriceDirPath()+'/'+str(id)
  #     res = open(path,'r').read()
      
  #     # am = self.getEntityAm(res,parseDay)
  #     # d = KdjParser.getD(parseDay,id)

  #     # r = am/d
  #     # r = d

  #     dayList = BaseParser.getPastTradingDayList(parseDay,5) 
  #     (v,v,ma) = self.getMAPrice(res,dayList)
  #     endPrice = self.getEndPriceOfDay(res,parseDay)

  #     r = ma/endPrice

  #     vList.append((id,r))

  #   # 排序
  #   sList = sorted(vList,key=lambda x: -x[1]) 
  #   # sList = sorted(vList,key=lambda x: x[1]) 
  #   print "sorted list:"
  #   print sList
  #   selectedList = sList[:num]

  #   print "\nselected list:"
  #   print selectedList
  #   l = []
  #   for item in selectedList:
  #     l.append(item[0])
  #   return l

  
  # 连阳
  def getContinuousYangXianNum(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,20) 
    dayList.reverse()
    num = 0
    for day in dayList:
      startPrice = self.getStartPriceOfDay(res,day)
      endPrice = self.getEndPriceOfDay(res,day)
      if endPrice > startPrice:
        num += 1
      else:
        break
    return num


  # 判断是否涨停
  def isUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPrice1 = self.getEndPriceOfDay(res,dayList[-2])
    endPrice2 = self.getEndPriceOfDay(res,dayList[-1])
    if endPrice1 == 0 or  endPrice2 == 0:
      return False
    r = (endPrice2 - endPrice1)/endPrice1
    if r < 0.095:
      return False
    return True

  

  def isRgb(self,res,day):
    R = 5
    G = 10
    B = 20

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if not ((maR > maG) and (maG > maB)):
      return False

    return True


  
  def parse(self,res,parseDay,id=''):
    rgbDays = 5
    dayList = self.getPastTradingDayList(parseDay,rgbDays)

    # 连续N天RGB
    for day in dayList:
      if not self.isRgb(res,day):
        return False

    # 今日最低价低于20日均线
    dayList = BaseParser.getPastTradingDayList(parseDay,20) 
    (v,v,ma) = self.getMAPrice(res,dayList)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    if minPrice > ma:
      return False

    return True


  # def parse(self,res,parseDay,id=''):
  #   # 参数检查
  #   startPrice = self.getStartPriceOfDay(res,parseDay)
  #   endPrice = self.getEndPriceOfDay(res,parseDay)
  #   minPrice = self.getMinPriceOfDay(res,parseDay)
  #   maxPrice = self.getMaxPriceOfDay(res,parseDay)
  #   if startPrice == 0 or endPrice == 0 or minPrice == 0 or maxPrice == 0:
  #     return False

  #   # 剔除新股
  #   if self.isNewStock(res,parseDay):
  #     return False

  #   # 阳线
  #   if not self.isYangXian(res,parseDay):
  #     return False

  #    # 实体振幅大于n%
  #   am = self.getEntityAm(res,parseDay)
  #   if (am <= 0.05):
  #     return False

  #   # # 最高价位于ma之下
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
  #   # (v,v,ma) = self.getMAPrice(res,dayList)
  #   # if endPrice >= ma:
  #   #   return False

  #   # # D低于
  #   # d = KdjParser.getD(parseDay,id)
  #   # if False == d:
  #   #   return False
  #   # if d >= 20:
  #   #   return False


  #   # am = self.getAm(res,parseDay)
  #   # if am <= 0.1:
  #   #   return False


  #   # D向上反转
  #   # -----------------------------------------------------------------
  #   # if not KdjParser.isDDeclineDeceleration(parseDay,id):
  #   #   return False
     

  #   # 剔除涨停
  #   # if self.isUpwardLimit(res,parseDay):
  #   #   return False

  
  #   # 5日线下K线
  #   # -----------------------------------------------------------------
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
  #   # lastDay = dayList[-2]




    

  #   # 振幅n日最大
  #   # am = (maxPrice - minPrice)/minPrice
  #   # maxAmOfDays = 0
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
  #   # for day in dayList:
  #   #   minP = self.getMinPriceOfDay(res,day)
  #   #   maxP = self.getMaxPriceOfDay(res,day)
  #   #   amOfDay = (maxP - minP)/minP
  #   #   if amOfDay > maxAmOfDays:
  #   #     maxAmOfDays = amOfDay
  #   # if am < maxAmOfDays:
  #   #   return False


   



  #   # 振幅大于n%
  #   # minP = minPrice
  #   # r = (maxPrice - minP)/minP
  #   # if (r <= 0.07):
  #   #   return False


    


  #   # K D J判断
  #   # days = 1
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,days)
  #   # dataOfDays = KdjParser.getKDJData(parseDay,id,days)
  #   # if False == dataOfDays:
  #   #   return False

  #   # k = float(dataOfDays[dayList[-1]][0])
  #   # d = float(dataOfDays[dayList[-1]][1])
  #   # j = float(dataOfDays[dayList[-1]][2])
  #   # # if j <= d:
  #   # #   return False
  #   # # if j >= 0:
  #   # if j >= -10:
  #   #   return False



  #   # J向上反转
  #   # if not KdjParser.isJUpwardReverse(parseDay,id):
  #   #   return False
    
  #   # JN
  #   # if not KdjParser.isJN(parseDay,id):
  #     # return False


  #   # JW
  #   # if not KdjParser.isJW(parseDay,id):
  #     # return False


  #   #  D向上反转
  #   # if not KdjParser.isDBottomReversal(parseDay,id):
  #   #   return False

  #   # KD金叉
  #   # if not KdjParser.isKdGoldCross(parseDay,id):
  #   #   return False


  #   # 5日量比
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,5)
  #   # mv5 = self.getMv(res,dayList)
  #   # v = self.getVolumeOfDay(res,parseDay)
  #   # if v/mv5 >= 0.5:
  #   #   return False

  #   # BIAS为正
  #   # if not BiasParser.isBiasNegative(parseDay,id):
  #   #   return False

  #   # 近20日上涨
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,60)
  #   # endPrice1 = self.getEndPriceOfDay(res,dayList[0])
  #   # endPrice2 = self.getEndPriceOfDay(res,dayList[-1])
  #   # if endPrice2 <= endPrice1:
  #   #   return False

  #   # 连阳
  #   # num = self.getContinuousYangXianNum(res,parseDay)
  #   # if num != 7: # 连阳数
  #   #   return False

  #   return True


if __name__ == '__main__':
  print 'RelativeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = RelativeParser(parseDay).getParseResult(True)
  print idList

















