#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-10
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
D低于20，且值变大
'''
class KdjParser(BaseParser):
  _tag = 'KdjParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 
  

  def printProcess(self,current,total):
    lastRate = round((current-1)*100.0/total,0)
    currentRate = round(current*100.0/total,0)
    if lastRate != currentRate:
      rate = str(int(currentRate)) 
      rate = rate.rjust(3,' ')
      s = ''
      s = s.rjust(int(currentRate),'.')
      s += ' -> '
      s = s.ljust(104,' ')
      s += rate + ' %'
      print s


  def getParseResult(self,isDump=False):
    idList = []
    num = 0
    kdjFileList = BaseParser.getKdjFileList()
    parsedNum = 0
    total = len(kdjFileList)
    for f in kdjFileList:
      try:
        self.printProcess(parsedNum,total)
        res = open(f,'r').read()
        ret = self.parse(res,self._parseDay)
        if ret:
          idList.append(f[-6:])
          num += 1
          print str(num) + ' ↗'
          parsedNum += 1
      except Exception, e:
        parsedNum += 1
        pass
        # print repr(e)

    if isDump:
      self.dumpIdList(idList)

    return idList


  def parse(self,res,parseDay,id=''):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 坏数据：个股交易日未必连续        
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      return False

    '''
      0       1       2
      K       D       J
    '''
    
    kOfParseDay = float(dataOfDays[parseDay][0])
    dOfParseDay = float(dataOfDays[parseDay][1])
    jOfParseDay = float(dataOfDays[parseDay][2])

    kOfLastDay = float(dataOfDays[dayList[0]][0])
    dOfLastDay = float(dataOfDays[dayList[0]][1])
    jOfLastDay = float(dataOfDays[dayList[0]][2])

    v = 20


    # 三线都小于20
    if kOfParseDay >= v:
      return False

    if dOfParseDay >= v:
      return False

    if jOfParseDay >= v:
      return False

    # K金叉D
    if not((kOfLastDay < dOfParseDay) and (kOfParseDay > dOfParseDay)):
      return False

    # J金叉D
    if not((jOfLastDay < dOfParseDay) and (jOfParseDay > dOfParseDay)):
      return False

    # # K在D之下
    # if kOfParseDay > dOfParseDay:
    #   return False

    # # J在D之上
    # if jOfParseDay < dOfParseDay:
    #   return False


    


    # # D小于20且变大，K、J变大但小于D
    # if dOfParseDay >= v:
    #   print 'dOfParseDay >= v'
    #   return False
    # if kOfParseDay <= kOfLastDay:
    #   print 'kOfParseDay <= kOfLastDay'
    #   return False
    # if dOfParseDay <= dOfLastDay:
    #   print 'dOfParseDay <= dOfLastDay'
    #   return False
    # if jOfParseDay <= jOfLastDay:
    #   print 'jOfParseDay <= jOfLastDay'
    #   return False
    # if kOfParseDay > dOfParseDay:
    #   print 'kOfParseDay > dOfParseDay'
    #   return False
    # if jOfParseDay > dOfParseDay:
    #   print 'jOfParseDay > dOfParseDay'
    #   return False

    # D上穿20
    # if dOfParseDay <= v:
    #   return False
    # if dOfLastDay >= v:
    #   return False

    # D小于20且变大
    # if dOfParseDay > v:
    #   return False
    # if dOfParseDay <= dOfLastDay:
    #   return False



    return True



if __name__ == '__main__':
  print 'KdjParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = KdjParser(parseDay).getParseResult(True)
  print idList

















