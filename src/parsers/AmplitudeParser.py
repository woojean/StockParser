#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-11-30
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
振幅
'''
class AmplitudeParser(BaseParser):
  _tag = 'AmplitudeParser'

  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 

  
  # # -------------------------------------------------------------------------------------
  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    # idFile = '振幅/振幅>=5%D<=20D向上/'+self._parseDay+'-AmplitudeParser.sel'

    idFile = '5日线下阳线/5日线下阳线/'+self._parseDay+'-AmplitudeParser.sel'
    # idFile = '5日线下阳线/5日线下阳线-振幅>5%/'+self._parseDay+'-AmplitudeParser.sel'

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
      
    print idList

    # 根据打分结果过滤
    idList = self.calcuR(idList,2)

    if isDump:
      self.dumpIdList(idList)

    return idList


  # -------------------------------------------------------------------------------------
  def calcuR(self,idList,num):
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      r = random.random()

      vList.append((id,r))

    # 排序
    sList = sorted(vList,key=lambda x: -x[1]) 
    # sList = sorted(vList,key=lambda x: x[1]) 
    print "sorted list:"
    print sList
    selectedList = sList[:num]

    print "\nselected list:"
    print selectedList
    l = []
    for item in selectedList:
      l.append(item[0])
    return l



  # -------------------------------------------------------------------------------------
  def parse(self,res,parseDay,id=''):
    # 剔除新股（含复牌股）
    # if self.isNewStock(res,parseDay):
    #   return False

    # 振幅>n%
    # am = self.getAm(res,parseDay)
    # if not am > 0.07:
    #   return False

    # 阳线
    if not self.isYangXian(res,parseDay):
      return False

    # # 最高价低于5日线
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if maxPrice > ma:
    #   return False


    # 最高价相对5日线向下乖离程度
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # r = (ma - maxPrice)/maxPrice
    # if r <= 0.02:
    #   return False

    
    # D向下
    # if not KdjParser.isDDownward(parseDay,id):
    #   return False

    # D向上
    # if not KdjParser.isDUpward(parseDay,id):
    #   return False

    # D低于
    # d = KdjParser.getD(parseDay,id)
    # if False == d:
    #   return False
    # if d > 30:
    #   return False

    # 收盘价低于5日线
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # endPrice = self.getEndPriceOfDay(res,parseDay)
    # if endPrice > ma:
    #   return False


    # 5日线在60日线上（对上升趋势的模拟）
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma5) = self.getMAPrice(res,dayList)
    # dayList = BaseParser.getPastTradingDayList(parseDay,60) 
    # (v,v,ma60) = self.getMAPrice(res,dayList)
    # if not ma5 > ma60:
    #   return False





    # 近3日有跌停
    # haveDownwardLimit = False
    # dayList = BaseParser.getPastTradingDayList(parseDay,3) 
    # for day in dayList:
    #   endPrice2 = self.getEndPriceOfDay(res,day)
    #   tDayList = BaseParser.getPastTradingDayList(day,2) 
    #   lastDay = tDayList[0]
    #   endPrice1 = self.getEndPriceOfDay(res,lastDay)
    #   if endPrice1 == 0:
    #     continue
    #   r = (endPrice2-endPrice1)/endPrice1
    #   if r < -0.095:
    #     haveDownwardLimit = True
    #     break
    # if not haveDownwardLimit:
    #   return False


    # 近3日盘中有跌停
    # haveTouchDownwardLimit = False
    # dayList = BaseParser.getPastTradingDayList(parseDay,3) 
    # for day in dayList:
    #   minPrice2 = self.getMinPriceOfDay(res,day)
    #   tDayList = BaseParser.getPastTradingDayList(day,2) 
    #   lastDay = tDayList[0]
    #   endPrice1 = self.getEndPriceOfDay(res,lastDay)
    #   if endPrice1 == 0:
    #     continue
    #   r = (minPrice2-endPrice1)/endPrice1
    #   if r < -0.095:
    #     haveTouchDownwardLimit = True
    #     break
    # if not haveTouchDownwardLimit:
    #   return False


    # 5，10，20三线空头排列
    # dayList = self.getPastTradingDayList(parseDay,5)
    # (v,v,ma5) = self.getMAPrice(res,dayList)
    # dayList = self.getPastTradingDayList(parseDay,10)
    # (v,v,ma10) = self.getMAPrice(res,dayList)
    # dayList = self.getPastTradingDayList(parseDay,20)
    # (v,v,ma20) = self.getMAPrice(res,dayList)
    # if not ((ma20 > ma10) and (ma10 > ma5)):
    #   return False

    
    # 盘中有跌停
    # haveTouchDownwardLimit = False
    # minPrice2 = self.getMinPriceOfDay(res,parseDay)
    # tDayList = BaseParser.getPastTradingDayList(parseDay,2) 
    # lastDay = tDayList[0]
    # endPrice1 = self.getEndPriceOfDay(res,lastDay)
    # if endPrice1 == 0:
    #   return False
    # r = (minPrice2-endPrice1)/endPrice1
    # if r > -0.09:
    #   return False



    # KD死叉
    # if not KdjParser.isKdDeathCross(parseDay,id):
    #   return False

    # # 3日内有SLOWKD死叉
    # days = 3
    # maDays = 5
    # if not KdjParser.haveSLOWKDDeathCross(parseDay,id,days,maDays):
    #   return False

    # # BIAS非三线为负
    # if not BiasParser.isBiasAllNegative(parseDay,id):
    #   return False

    # D向下反转
    # if not KdjParser.isDDownwardReverse(parseDay,id):
    #   return False


    # 连续3日振幅>=n%
    # dayList = self.getPastTradingDayList(parseDay,5)
    # for day in dayList:
    #   am = self.getAm(res,day)
    #   if am < 0.07:
    #     return False


    # 买入日限制
    #----------------------------------------------------
    # dayList = self.getNextTradingDayList(parseDay,1)
    # nextDay = dayList[0]
    # minPrice = self.getMinPriceOfDay(res,nextDay)
    # startPrice = self.getStartPriceOfDay(res,nextDay)
    # r = (minPrice - startPrice)/startPrice
    # if not r == 0:
    # # if not ((r > -0.1) and (r <= -0.08) ):
    #   return False


    return True




if __name__ == '__main__':
  print 'AmplitudeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = AmplitudeParser(parseDay).getParseResult(True)
  print idList

















