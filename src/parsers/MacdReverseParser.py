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
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
MACD反转判断
'''
class MacdReverseParser(BaseParser):
  _tag = 'MacdReverseParser'
  _days = 5
  
  def __init__(self,parseDay,days = 5):
    self._days = days
    BaseParser.__init__(self,parseDay) 
  
  def getParseResult(self,isDump=False):
    idList = []
    num = 0
    macdFileList = BaseParser.getMacdFileList()
    for f in macdFileList:
      try:
        res = open(f,'r').read()
        ret = self.parse(res,self._parseDay)
        if ret:
          idList.append(f[-6:])
          num += 1
          print str(num) + ' ↗'
      except Exception, e:
        pass
        print repr(e)

    if isDump:
      self.dumpIdList(idList)

    return idList


  def parse(self,res,parseDay,id=''):
    dayList = BaseParser.getPastTradingDayList(parseDay,self._days)
    macdList = eval(res[26:-1])
    days = {}
    for item in macdList:
      for d in dayList:
        if d == item['time']:
          days[d] = eval(item['macd'])

    # 坏数据：个股交易日未必连续        
    if (len(days)<1) or (len(dayList) != len(days)):
      return False

    '''
      0       1       2
      0.070,  0.048,  0.044
      DIF     DEA     MACD
    '''
    
    match = True

    # 前4天MACD递减
    daysNum = len(dayList)
    for j in xrange(0, daysNum-2):
      # 前一日 > 后一日,必须递减
      if (float(days[dayList[j]][2]) <= float(days[dayList[j+1]][2])):
        match = False
        break
    

    # 最后2天MACD反转
    if (float(days[dayList[-2]][2]) >= float(days[dayList[-1]][2])):
      match = False

    if not match:
      return False

    return True



if __name__ == '__main__':
  print 'MacdReverseParser'
  
  days = 10

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MacdReverseParser(parseDay,days).getParseResult(True)
  print idList

















