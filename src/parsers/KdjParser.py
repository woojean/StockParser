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
class KdjParser(BaseParser):
  _tag = 'KdjParser'
  
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

  @staticmethod
  def getMutationScore(id,parseDay):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误，当做下降处理
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    d1 = float(dataOfDays[dayList[-3]][1])
    d2 = float(dataOfDays[dayList[-2]][1])
    d3 = float(dataOfDays[dayList[-1]][1])
    
    # 新股
    if d1 >= 100 or d2 >= 100 or d3 >= 100:
      return 0

    # 有顶
    if d1>d2:
      return 0
    if d3>d2:
      return 0

    # 陡：2日D增幅不小于2
    dv1 = d2 - d1

    # 急：拐弯急
    dv2 = d2 - d3

    # 高：当前成熟度
    h = 100.0 - d3

    # 分
    # score = (d2-d1)*(d2-d3)*(100-d3)
    # score = dv1 * dv2 * (100.0 - d3)

    # score = (d2-d1)*(d2-d3)*(10-d3/10)
    score = dv1 * dv2 * (10 - d3/10.0)

    # print score

    return score


  @staticmethod
  def isSpires(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误，当做下降处理
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    d1 = float(dataOfDays[dayList[-3]][1])
    d2 = float(dataOfDays[dayList[-2]][1])
    d3 = float(dataOfDays[dayList[-1]][1])
    
    if d1 >= 100 or d2 >= 100 or d3 >= 100:
      print '-------------------------------------------------->'
      return False

    # 有顶
    # d1 <= d2 >= d3
    if d1>d2:
      return False
    if d3>d2:
      return False

    # # score = dv * r

    # # 陡：2日D增幅不小于2
    # dv1 = d2 - d1

    # # 急：拐弯急
    # dv2 = d2 - d3

    # # 高：当前成熟度
    # h = (100 - d)/10.0

    # # 分
    # score = dv1 * dv2 * h

    return True


  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    idFile = 'd/'+self._parseDay+'-KdjParser.sel'
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


    # 打分
    idList = self.calcuR(idList,1)

    if isDump:
      self.dumpIdList(idList)

    return idList
  


  # def getParseResult(self,isDump=False):
  #   idList = []
  #   num = 0
  #   kdjFileList = BaseParser.getKdjFileList()
  #   parsedNum = 0
  #   total = len(kdjFileList)
  #   for f in kdjFileList:
  #     try:
  #       id = f[-6:]
  #       self.printProcess(parsedNum,total)
  #       res = open(f,'r').read()
  #       ret = self.parse(res,self._parseDay,id)
  #       if ret:
  #         idList.append(id)
  #         num += 1
  #         print str(num) + ' ↗'
  #         parsedNum += 1
  #     except Exception, e:
  #       parsedNum += 1
  #       pass
  #       # print repr(e)

  #   # 打分
  #   # idList = self.calcuR(idList,1)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList



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


  def isDBottomReversal(self,res,parseDay,id=''):
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])
    # 坏数据：个股交易日未必连续        
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      return False
    d1 = float(dataOfDays[dayList[0]][1])
    d2 = float(dataOfDays[dayList[1]][1])
    d3 = float(dataOfDays[dayList[2]][1])
    if not ((d2<d1)and(d2<d3)):
      return False
    return True


  # 顶部反转
  @staticmethod
  def isDTopReversal(parseDay,id=''):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      return False
    d1 = float(dataOfDays[dayList[0]][1])
    d2 = float(dataOfDays[dayList[1]][1])
    d3 = float(dataOfDays[dayList[2]][1])
    if not ((d2>d1)and(d2>d3)):
      return False
    return True


  @staticmethod
  def getPastWkKdjList(parseDay,id,num = 1):
    path = Tools.getKdjWkDataPath()+'/' +id
    res = open(path,'r').read()
    # dayList = BaseParser.getPastTradingDayList(parseDay,num)
    kdjList = eval(res[26:-1])
    total = len(kdjList)
    if total < 1:
      return False

    index = 0
    for i in xrange(0,total-1):
      # print kdjList[i-1]['time'],parseDay,kdjList[i]['time']
      if kdjList[i]['time'] >= parseDay and kdjList[i-1]['time'] <= parseDay:
        index = i
        # print 'here'
        break
    
    # print index
    if index == 0:
      return False

    wkKdjList = kdjList[(index-num):index]
    return wkKdjList


  @staticmethod
  def isDUpwardAndNotTooHigh(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # print dataOfDays
    d1 = float(dataOfDays[dayList[-2]][1])
    d = float(dataOfDays[dayList[-1]][1])

    # 数据错误，当做下降处理
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    # d在下降
    if d < d1: 
      return False
    
    # d大于70
    if d > 70:
      return False

    return True


  @staticmethod
  def dIsLow(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误，当做下降处理
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    d = float(dataOfDays[dayList[-1]][1])

    # d低于某个值
    if d > 20:
      return False

    return True


  @staticmethod
  def dIsDangerous(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误，当做下降处理
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    d1 = float(dataOfDays[dayList[-2]][1])
    d2 = float(dataOfDays[dayList[-1]][1])

    # d低于某个值
    if (d2 > 70) and (d2 < d1):
      return True

    return False


  # 近n日有SLOWKD死叉
  @staticmethod
  def haveDeathCross(parseDay,id,days,maDays):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,20)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误，当做无死叉，人工判断
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    cDayList = BaseParser.getPastTradingDayList(parseDay,days)
    haveDeathCross = False
    for i in xrange(1,days-1):
      preD = float(dataOfDays[cDayList[i-1]][1])
      nowD = float(dataOfDays[cDayList[i]][1])
      sumD = 0
      maDayList = BaseParser.getPastTradingDayList(cDayList[i],maDays)
      for day in maDayList:
        d = float(dataOfDays[day][1])
        sumD += d
      maD = sumD/maDays
      if ((preD > maD) and (nowD < maD)):
        haveDeathCross = True
        break

    if haveDeathCross:
      return True

    return False




  @staticmethod
  def isKdj(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误，当做未金叉处理
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    # D在20之下
    # dayLimit = 20
    # d = float(dataOfDays[dayList[-1]][1])
    # if d > dayLimit or d < 1:  # d大于20，或d数据错误
    #   return False

    k1 = float(dataOfDays[dayList[-2]][0])
    k2 = float(dataOfDays[dayList[-1]][0])
    d = float(dataOfDays[dayList[-1]][1])

    if not((k1 < d) and (k2 > d)):
      return False

    return True

  # D低于某个值
  @staticmethod
  def isDLow(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False

    # D在指定值之下
    dayLimit = 20
    d = float(dataOfDays[dayList[-1]][1])
    if d > dayLimit or d < 1:  # d大于20，或d数据错误
      return False

    return True



  # J、K、D当日多头排列，且相对前一日都在上涨
  @staticmethod
  def isKdjBull(parseDay,id):
    path = Tools.getKdjDataPath()+'/' +id
    res = open(path,'r').read()
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 数据错误
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):  
      return False


    k1 = float(dataOfDays[dayList[-2]][0])
    k2 = float(dataOfDays[dayList[-1]][0])
    d1 = float(dataOfDays[dayList[-2]][1])
    d2 = float(dataOfDays[dayList[-1]][1])
    j1 = float(dataOfDays[dayList[-2]][2])
    j2 = float(dataOfDays[dayList[-1]][2])

    # D在20之下
    dayLimit = 20
    if d2 > dayLimit or d2 < 1:  # d大于20，或d数据错误
      return False

    if (k2 <= k1) or (d2 <= d1) or (j2 <= j1):
      return False

    # J K D
    if not ((j2 > k2) and (k2 > d2)):
      return False

    return True

  
  


  def parse(self,res,parseDay,id):
    if not self.isSpires(parseDay,id):
      return False
    return True


  # D低于20，J金叉D
  def parse3(self,res,parseDay,id):
    # D空中加油
    dayList = BaseParser.getPastTradingDayList(parseDay,20)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 坏数据：个股交易日未必连续        
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      # print 'len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)'
      return False

    # d15 d14 d13 d12 d11 d10 d9 d8 d7 d6 d5 d4 d3 d2 d1
    d1 = float(dataOfDays[dayList[-1]][1])
    d2 = float(dataOfDays[dayList[-2]][1])
    d3 = float(dataOfDays[dayList[-3]][1])
    d10 = float(dataOfDays[dayList[-10]][1])
    d15 = float(dataOfDays[dayList[-15]][1])

    # d1 > d2
    if not d1 > d2:
      return False

    # d3 > d2
    if not d3 > d2:
      return False

    # d2 > d15
    if not d2 > d15:
      return False

    # d10 > d15
    if not d10 > d15:
      return False

    return True

    # D在20之下，K金叉D
    # ------------------------------------------------------------------
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # kdjList = eval(res[26:-1])
    # dataOfDays = {}
    # for item in kdjList:
    #   for d in dayList:
    #     if d == item['time']:
    #       dataOfDays[d] = eval(item['kdj'])

    # # 坏数据：个股交易日未必连续        
    # if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
    #   # print 'len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)'
    #   return False

    # dayLimit = 20

    # # D在20之下
    # d = float(dataOfDays[dayList[-1]][1])
    # if d > dayLimit or d < 1:  # d大于20，或d数据错误
    #   return False

    # # K金叉D
    # # j1 = float(dataOfDays[dayList[-2]][2])
    # # j2 = float(dataOfDays[dayList[-1]][2])
    # # if not ((j1 < d) and (j2 > d)):
    #   # return False

    # k1 = float(dataOfDays[dayList[-2]][0])
    # k2 = float(dataOfDays[dayList[-1]][0])
    # if not ((k1 < d) and (k2 > d)):
    #   return False

    # return True




  # 日、周线D都在5日均线上，且和5日均线的距离都增加，且都小于60，且都大于前一日
  def parse2(self,res,parseDay,id):
    # print 'parse'
    # 取参数
    # ---------------------------------------------------------------------
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    kdjList = eval(res[26:-1])
    dataOfDays = {}
    for item in kdjList:
      for d in dayList:
        if d == item['time']:
          dataOfDays[d] = eval(item['kdj'])

    # 坏数据：个股交易日未必连续        
    if (len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)):
      # print 'len(dataOfDays)<1) or (len(dayList) != len(dataOfDays)'
      return False

    '''
      0       1       2
      K       D       J
    '''
    

    dayLimit = 50
    weekLimit = 50
    maDays = 5

    # 日线
    # print '日线'
    # ---------------------------------------------------------------------
    d1 = float(dataOfDays[dayList[-2]][1])
    if d1 >= dayLimit or d1 < 1:
      return False

    d2 = float(dataOfDays[dayList[-1]][1])
    if d2 >= dayLimit or d2 < 1:
      return False

    if d2 <= d1:
      return False
    
    dayList1 = BaseParser.getPastTradingDayList(dayList[-2],maDays)
    sumD1 = 0
    for day in dayList1:
      d = float(dataOfDays[day][1])
      sumD1 += d
    maD1 = sumD1/maDays
    if d1<maD1:
      return False

    dayList2 = BaseParser.getPastTradingDayList(dayList[-1],maDays)
    sumD2 = 0
    for day in dayList2:
      d = float(dataOfDays[day][1])
      sumD2 += d
    maD2 = sumD2/maDays
    if d2 <maD2:
      return False
    
    if((d2-maD2) < (d1-maD1)):  # 间距缩小
      return False


    # 周线
    # print '周线'
    # ---------------------------------------------------------------------
    pastWkKdjList = KdjParser.getPastWkKdjList(parseDay,id,10)

    wd1 = float(eval(pastWkKdjList[-2]['kdj'])[1])
    if wd1 >= weekLimit or wd1 <1:  
      # print 'wd1 >= v'
      return False
    
    wd2 = float(eval(pastWkKdjList[-1]['kdj'])[1])
    if wd2 >= weekLimit or wd2 <1:  
      # print 'wd2 >= v'
      return False

    if wd2 <= wd1:
      return False

    sumWd1 = 0
    pastWkKdjList1 = KdjParser.getPastWkKdjList(dayList[-2],id,maDays)
    for item in pastWkKdjList1:
      sumWd1 += float(eval(item['kdj'])[1])
    maWD1 = float(sumWd1/maDays) 
    if wd1 < maWD1 or maWD1 <1: 
      # print 'wd1 < maWD1'
      return False


    
    sumWd2 = 0
    pastWkKdjList2 = KdjParser.getPastWkKdjList(dayList[-1],id,maDays)
    for item in pastWkKdjList2:
      sumWd2 += float(eval(item['kdj'])[1])
    maWD2 = float(sumWd2/maDays) 
    if wd2 < maWD2 or maWD2 <1: 
      # print 'wd2 < maWD2'
      return False
    
    if ((wd2 - maWD2)< (wd1 - maWD1)):
      # print 'wd2 - maWD2'
      return False

    print wd1,maWD1,wd2,maWD2

    return True



if __name__ == '__main__':
  print 'KdjParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = KdjParser(parseDay).getParseResult(True)
  print idList
  
  # ret = KdjParser.getPastWkKdjList('2018-09-20','000001',3)
  # print ret
















