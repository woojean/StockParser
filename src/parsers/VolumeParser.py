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


  # def parse(self,res,parseDay,id=''):
  #   # 近期有连板（剔除一字板）
  #   days = 20
  #   if not self.recentlyHaveContinusUpwardLimit(res,parseDay,days):
  #     return False
    

  #   # 相对前一日缩量
  #   # -------------------------------------------------------
  #   if not self.isVolumnShrink(res,parseDay):
  #     return False


  #   return True

  

  def parse(self,res,parseDay,id=''):

    # 相对前一日缩量
    # -------------------------------------------------------
    # r = self.getVolumnShrinkRate(res,parseDay)
    # if not r <= 0.8:
    #   return False

    
    # D 
    # -------------------------------------------------------
    if not KdjParser.isDUpward(parseDay,id):
      return False

    d = KdjParser.getD(parseDay,id)
    # if not ((d > 30) and (d < 60)):
    if not (d < 20):
      return False


    # 近n日涨停数达到一定值
    # -------------------------------------------------------
    days = 120
    minUpwardLimitNum = 3
    upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
    if not upwardLimitNum >= minUpwardLimitNum:
      return False


    return True





if __name__ == '__main__':
  print 'VolumeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = VolumeParser(parseDay).getParseResult(True)
  print idList

















