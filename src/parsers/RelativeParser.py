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
import random
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
  #   idFile = '振幅/振幅>=5%阳线最高价低于5日线'+self._parseDay+'-AmplitudeParser.sel'
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
  #   # idList = self.calcuR(idList,10)

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

  #     # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
  #     # (v,v,ma) = self.getMAPrice(res,dayList)
  #     # endPrice = self.getEndPriceOfDay(res,parseDay)

  #     # r = ma/endPrice

  #     # vList.append((id,r))

  #     days = 5
  #     r = self.getGrOfDays(res,parseDay,days)

  #     # r = random.random()
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

  
  def parse(self,res,parseDay,id=''):
    
    # 非一字板涨停
    if not self.isUpwardLimit(res,parseDay):
      return False

    # # 阳线
    # # -------------------------------------------------------
    # if not self.isYangXian(res,parseDay):
    #   return False


    # # 最高价低于5日线
    # # -------------------------------------------------------
    # if not self.isMaxPriceUnderMa(res,parseDay,5):
    #   return False


    # 前一日缩量：量缩至5日线下
    # -------------------------------------------------------
    # dayList = self.getPastTradingDayList(parseDay,2)
    # lastDay = dayList[0]
    # if not self.isVolumnUnderMv(res,lastDay,5):
    #   return False
    

    # 反转：今日发生最低价向上反转
    # -------------------------------------------------------
    # if not self.isMinPriceUpwardReverse(res,parseDay):
    #   return False

    # 强势：5，10，20三线多头排列
    # -------------------------------------------------------
    # if not self.isInUpTrend(res,parseDay):
    #   return False


    # 中线趋势向上
    # -------------------------------------------------------
    # if not self.isMaInUpTrend(res,parseDay,20,60):
    #   return False


    # 近n日涨停数达到一定值
    # -------------------------------------------------------
    # days = 120
    # minUpwardLimitNum = 1
    # upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
    # if not upwardLimitNum >= minUpwardLimitNum:
    #   return False

    # 最高价在60日线上
    # -------------------------------------------------------
    # if not self.isMinPriceOnMa(res,parseDay,60):
    #   return False

    return True


  def parse2(self,res,parseDay,id=''):

    # 阳线
    # -------------------------------------------------------
    if not self.isYangXian(res,parseDay):
      return False


    # 最高价低于5日线
    # -------------------------------------------------------
    if not self.isMaxPriceUnderMa(res,parseDay,5):
      return False


    # 中线趋势向上
    # -------------------------------------------------------
    # if not self.isMaInUpTrend(res,parseDay,20,60):
    #   return False


    # 振幅
    am = self.getAm(res,parseDay)
    if not am >= 0.05:
      return False


    # 放量
    # -------------------------------------------------------
    # if self.isVolumnUnderMv(res,parseDay,5):
    #   return False



    # 强势：5，10，20三线多头排列
    # -------------------------------------------------------
    # if not self.isRgb(res,parseDay):
    #   return False


    # 20日均线向上
    # if not self.isMaUpward(res,parseDay,5):
    #   return False
    

    # 近n日涨停数达到一定值
    # -------------------------------------------------------
    # days = 120
    # minUpwardLimitNum = 1
    # upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
    # if not upwardLimitNum >= minUpwardLimitNum:
    #   return False
 


    return True




  
  # def parse(self,res,parseDay,id=''):
  #   # days = 5
  #   # gr = self.getGrOfDays(res,parseDay,days)
  #   # if gr <= 0.1:
  #   #   return False

  #   # 最近9天有且仅有6根阳线，且第10天阴线
  #   # if not self.isYangXian(res,parseDay):
  #   #   return False

  #   # dayList = BaseParser.getPastTradingDayList(parseDay,10)
  #   # if self.isYangXian(res,dayList[0]):
  #   #   return False

    
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,9)
  #   # yangXianNum = 0
  #   # for day in dayList:
  #   #   if self.isYangXian(res,day):
  #   #     yangXianNum += 1
  #   # if yangXianNum != 6:
  #   #   return False
    
  #   # # 流通市值小于50亿
  #   # basicInfo = BaseParser.getBasicInfoById(id)
  #   # mvc = float(basicInfo[45])
  #   # if mvc < 1:
  #   #   return False # 错误数据
    
  #   # if mvc > 5000000000:
  #   #   return False

  #   # 换手率大于1%
  #   # changeRate = float(self.getChangeRateOfDay(res,parseDay))
  #   # if changeRate < 1.0:
  #   #   return False



  #   # 涨停板（排除一字板）
  #   # if not self.isContinusUpwardLimit(res,parseDay):
  #   #   return False
    

  #   # # # 量缩至5日均量线下
  #   # # # -------------------------------------------------------
  #   # days = 5
  #   # if not self.isVolumnUnderMv(res,parseDay,days):
  #   #   return False

  #   # # D
  #   # isDUpward = KdjParser.isDUpward(parseDay,id)
  #   # d = KdjParser.getD(parseDay,id)
  #   # if (not isDUpward) and (not d < 20):
  #   #   return False


  #   # # # 近n日涨停数达到一定值
  #   # # # -------------------------------------------------------
  #   # days = 120
  #   # minUpwardLimitNum = 6
  #   # upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
  #   # if not upwardLimitNum >= minUpwardLimitNum:
  #   #   return False


  #   # # 连板股 + 缩量阴线
  #   # dayList = BaseParser.getPastTradingDayList(parseDay,2)
  #   # lastDay = dayList[0]

  #   # # 阴线
  #   # if self.isYangXian(res,parseDay):
  #   #   return False


  #   # if not self.isContinusUpwardLimit(res,lastDay):
  #   #   return False

  #   # # 缩量
  #   # v1 = self.getVolumeOfDay(res,lastDay)
  #   # v2 = self.getVolumeOfDay(res,parseDay)
  #   # if not v2 < v1:
  #   #   return False

    
  #   # # DV
  #   # if not KdjParser.isDUpwardReverse(parseDay,id):
  #   #   return False

  #   # # D < 20
  #   # d = KdjParser.getD(parseDay,id)
  #   # if False == d:
  #   #   return False
  #   # if d >= 20:
  #   #   return False



  #   # 近期最大振幅
  #   # days = 60
  #   # am = getAmplitudeOfDays(res,parseDay,days)
  #   # if not am < 1:
  #   #   return False


  #   # # 最高价低于MA
  #   # if not self.isMaxPriceUnderMa(res,parseDay,5):
  #   #   return False

   

  #   # # 量缩至5日均量线下
  #   # # -------------------------------------------------------
  #   # days = 5
  #   # if not self.isVolumnUnderMv(res,parseDay,days):
  #   #   return False

  #   # # 振幅
  #   # am = self.getAm(res,parseDay)
  #   # if not am >= 0.05:
  #   #   return False

  #   # # 近n日涨停数达到一定值
  #   # # -------------------------------------------------------
  #   # days = 120
  #   # minUpwardLimitNum = 1
  #   # upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
  #   # if not upwardLimitNum >= minUpwardLimitNum:
  #   #   return False




  #   # # 剔除新股（含复牌股）
  #   # if self.isNewStock(res,parseDay):
  #   #   return False

    
  #   # # 20日线向上
  #   # if not self.isMaUpward(res,parseDay,20):
  #   #   return False


    


  #   return True




  # def parse(self,res,parseDay,id=''):
    # # 剔除新股（含复牌股）
    # if self.isNewStock(res,parseDay):
    #   return False

    # # 涨停板（排除一字板）
    # if not self.isUpwardLimit(res,parseDay):
    #   return False

    # 相对前一日放量
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # lastDay = dayList[0]
    # vOfLastDay = self.getVolumeOfDay(res,lastDay)
    # v = self.getVolumeOfDay(res,parseDay)
    # if v <= vOfLastDay:
    #   return False


    # 跳空缺口
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # lastDay = dayList[0]
    # maxPrice1 = self.getMaxPriceOfDay(res,lastDay)
    # minPrice2 = self.getMinPriceOfDay(res,parseDay)
    # if not minPrice2 > maxPrice1:
    #   return False

    # D < 20
    # d = KdjParser.getD(parseDay,id)
    # if False == d:
    #   return False
    # if d >= 20:
    #   return False

    # 振幅
    # am = self.getAm(res,parseDay)
    # if am <= 0.1:
    #   return False

    # 首板
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # if self.isUpwardLimit(res,dayList[0]):
    #   return False
    
    # 2板
    # dayList = BaseParser.getPastTradingDayList(parseDay,3)
    # if not self.isUpwardLimit(res,dayList[1]):
    #   return False
    # if self.isUpwardLimit(res,dayList[0]):
    #   return False


    # DV
    # if not KdjParser.isDUpwardReverse(parseDay,id):
    #   return False

    # D下降
    # if KdjParser.isDUpward(parseDay,id):
    #   return False

    # 非连板，且10日内有涨停
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # if self.isUpwardLimit(res,dayList[0]):
    #   return False
    # haveUpwardLimit = False
    # dayList = BaseParser.getPastTradingDayList(parseDay,10)
    # dayList = dayList[:-2]
    # for day in dayList:
    #   if self.isUpwardLimit(res,day):
    #     haveUpwardLimit = True
    #     break
    # if not haveUpwardLimit:
    #   return False
    

    # 近20日最高价
    # if not self.isMaxPriceOfDays(res,parseDay,60):
    #   return False

    # 两个涨停板夹一个阴线
    # dayList = BaseParser.getPastTradingDayList(parseDay,3)
    # if not self.isUpwardLimit(res,dayList[0]):
    #   return False
    # startPrice = self.getStartPriceOfDay(res,dayList[1])
    # endPrice = self.getEndPriceOfDay(res,dayList[1])
    # if not endPrice < startPrice:
    #   return False


    # 穿头破脚（阳包阴）
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # startPrice1 = self.getStartPriceOfDay(res,dayList[0])
    # endPrice1 = self.getEndPriceOfDay(res,dayList[0])
    # if not endPrice1 < startPrice1:
    #   return False
    # startPrice2 = self.getStartPriceOfDay(res,parseDay)
    # endPrice2 = self.getEndPriceOfDay(res,parseDay)
    # if not ((startPrice2 < endPrice1) and (endPrice2 > startPrice1)):
    #   return False

    


    # 量大于MV5
    # dayList = BaseParser.getPastTradingDayList(parseDay,5)
    # mv = self.getMaVolume(res,dayList)
    # v = self.getVolumeOfDay(res,parseDay)
    # if not v > 3*mv:
    #   return False

    # KD金叉
    # if not KdjParser.isKdGoldCross(parseDay,id):
    #   return False

    # 秃底
    # startPrice = self.getStartPriceOfDay(res,parseDay)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # if not startPrice == minPrice:
    #   return False


    # 下引线长度占总长度超过30%
    # startPrice = self.getStartPriceOfDay(res,parseDay)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # endPrice = self.getEndPriceOfDay(res,parseDay)
    # totalLength = endPrice - minPrice
    # downLineLength = startPrice - minPrice
    # r = downLineLength/totalLength
    # if not ((r > 0) and (r <0.1)):
    #   return False
    

    # 昨日跌停
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # if not self.isDownwardLimit(res,dayList[0]):
    #   return False
    

    # 昨日一字板涨停
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # if self.isOneLineUpwardLimit(res,dayList[0]):
    #   return False


    # 非20日最高价
    # if self.isMaxPriceOfDays(res,parseDay,20):
    #   return False

    # 最低价为近20日最低价
    # if not self.haveMinPriceOfDays(res,parseDay,10):
    #   return False


    # return True

  
  # def parse(self,res,parseDay,id=''):
    # 剔除新股（含复牌股）
    # if self.isNewStock(res,parseDay):
    #   return False

    

    # # 振幅
    # am = self.getAm(res,parseDay)
    # if am <= 0.05:
    #   return False

    # J > D
    # j = KdjParser.getJ(parseDay,id)
    # d = KdjParser.getD(parseDay,id)
    # if False == j or False == d:
    #   return False
    # if not (j-d > 50):
    #   return False

    # J>70，J上升，J>D，10日涨幅低于10%
    # dayList = BaseParser.getPastTradingDayList(parseDay,10)
    # endPrice1 = self.getEndPriceOfDay(res,dayList[0]) 
    # endPrice2 = self.getEndPriceOfDay(res,dayList[-1]) 
    # if endPrice1 == 0:
    #   return False
    # r = (endPrice2 - endPrice1)/endPrice1
    # if r > 0.1:
    #   return False
    # # J向上
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # j1 = KdjParser.getJ(dayList[0],id)
    # j2 = KdjParser.getJ(dayList[1],id)
    # d2 = KdjParser.getD(dayList[1],id)
    # if j2 < 80:
    #   return False
    # if j2 < j1:
    #   return False
    # if j2 < d2:
    #   return False

    # J > 80
    # j = KdjParser.getJ(parseDay,id)
    # if False == j:
    #   return False
    # if not j > 80:
    #   return False


    # return True


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

















