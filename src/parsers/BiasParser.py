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
from common import Tools

reload(sys)
sys.setdefaultencoding('utf-8')

'''
D低于20，且值变大
'''
class BiasParser(BaseParser):
  _tag = 'BiasParser'
  
  def __init__(self,parseDay,id=''):
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



  # def getParseResult(self,isDump=False):
  #   print '***************************************************************************'
  #   print 'In custom mode'
  #   print '***************************************************************************'
  #   idFile = 'd/'+self._parseDay+'-KdjParser.sel'
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


  #   # 打分
  #   # idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList
  


  def getParseResult(self,isDump=False):
    idList = []
    num = 0
    biasFileList = BaseParser.getBiasFileList()
    parsedNum = 0
    total = len(biasFileList)
    for f in biasFileList:
      try:
        id = f[-6:]
        self.printProcess(parsedNum,total)
        res = open(f,'r').read()
        ret = self.parse(res,self._parseDay,id)
        if ret:
          idList.append(id)
          num += 1
          print str(num) + ' ↗'
          parsedNum += 1
      except Exception, e:
        parsedNum += 1
        pass
        # print repr(e)

    # 打分
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

  #   # 根据打分结果过滤
  #   idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)
  #   return idList


  # 打分
  def calcuR(self,idList,num):
    maDays = 10  # 均线
    vList = []
    for id in idList:
      score = KdjParser.getMutationScore(id,parseDay)
      vList.append((id,score))

    # 排序
    sList = sorted(vList,key=lambda x: -x[1]) # 倒序
    print "sorted list:"
    print sList
    selectedList = sList[:num]

    print "\nselected list:"
    print selectedList
    l = []
    for item in selectedList:
      l.append(item[0])
    return l

  
  @staticmethod
  def isBiasMinOfDays(parseDay,days,id):

    path = Tools.getBiasDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    biasList = eval(res[26:-1])
    dataOfDays = {}
    for item in biasList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['bias'])

    # 坏数据：个股交易日未必连续        
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      # print 'len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)'
      return False


    # bias n日最低
    biasIsMin = True
    bias = float(dataOfDays[parseDay][1])
    for day,data in dataOfDays.items():
      theBias = float(dataOfDays[day][1])
      if theBias < bias:
        biasIsMin = False
        break

    if not biasIsMin:
      return False

    return True


  @staticmethod
  def isBiasNegative(parseDay,id):
    path = Tools.getBiasDataPath()+'/' +id
    try:
      res = open(path,'r').read()
      if len(res) < 50:
        return True # 交由人工判断

      dayList = BaseParser.getPastTradingDayList(parseDay,2)
      biasList = eval(res[26:-1])
      dataOfDays = {}
      for item in biasList:
        for d in dayList:
          if d == item['time']:
            dataOfDays[d] = eval(item['bias'])
    except Exception, e:
      pass
      # print repr(e)
      return True

    # 坏数据：个股交易日未必连续        
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      # print 'len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)'
      return True  # 交由人工判断


    # bias n日最低
    bias6 = float(dataOfDays[parseDay][0])
    bias12 = float(dataOfDays[parseDay][1])
    bias24 = float(dataOfDays[parseDay][2])
   
    if bias6 >= 0  or bias12 >= 0 or bias24 >= 0:
      return False

    return True


  def parse(self,res,parseDay,id):
    days = 20 # n日最低

    biasIsMin = BiasParser.isBiasMinOfDays(parseDay,days,id)

    if not biasIsMin:
      return False

    return True


 




if __name__ == '__main__':
  print 'BiasParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = BiasParser(parseDay).getParseResult(True)
  print idList
  
  # ret = BiasParser.getPastWkKdjList('2018-09-20','000001',3)
  # print ret
















