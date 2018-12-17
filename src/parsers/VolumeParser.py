#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-12-15 04:00
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
缩量
'''
class VolumeParser(BaseParser):
  _tag = 'VolumeParser'

  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 


  # def getParseResult(self,isDump=False):
  #   print '***************************************************************************'
  #   print 'In custom mode'
  #   print '***************************************************************************'
  #   # idFile = '缩量/MA20上升缩量-阳线/'+self._parseDay+'-VolumeParser.sel'
  #   idFile = '缩量/MA20上升缩量/'+self._parseDay+'-VolumeParser.sel'
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
  #   # idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList




  
  def parse(self,res,parseDay,id=''):
    
    # 20日线向上
    # -------------------------------------------------------
    if not self.isMaUpward(res,parseDay,20):
      return False


    # 60日线向上
    # -------------------------------------------------------
    if not self.isMaUpward(res,parseDay,60):
      return False
    

    # 20日线在60日线上方
    # -------------------------------------------------------
    dayList = BaseParser.getPastTradingDayList(parseDay,20)
    (v,v,ma20) = self.getMAPrice(res,dayList)
    dayList = BaseParser.getPastTradingDayList(parseDay,60)
    (v,v,ma60) = self.getMAPrice(res,dayList)
    if ma20 < 0 or ma60<0:
      return False
    if not ma20 > ma60:
      return False


    # 缩量
    # -------------------------------------------------------
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    v1 = self.getVolumeOfDay(res,lastDay)
    v2 = self.getVolumeOfDay(res,parseDay)
    if not v2 < v1:
      return False


    return True





if __name__ == '__main__':
  print 'VolumeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = VolumeParser(parseDay).getParseResult(True)
  print idList

















