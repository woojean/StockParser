#coding:utf-8
#!/usr/bin/env python
import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser
from parsers import PenetrateUpwardMa20Parser

def getEnterListFiles():
  enterListDirPath = Tools.getEnterListDirPath()
  enterListFileList = []
  for root,dirs,files in os.walk(enterListDirPath):
    for f in files:
      if f =='.DS_Store':
        continue
      try:
        path = root + '/' + f
        enterListFileList.append(path)
      except Exception, e:
        pass
        # print repr(e)
  return enterListFileList


def printProcess(current,total):
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


def traceEnterList(f):
  ret = {}
  parser = f.split('/')[-1][11:-4]
  parseDay = f.split('/')[-1][:10]
  idList = open(f,'r').read().split(',')
  #idList = idList[:2]
  #if len(idList) > 2:
  #  idList = random.sample(idList, 2)
  ret['parser'] = parser
  ret['parseDay'] = parseDay
  ret['idList'] = []

  for id in idList:
    try:
      r = trace(id,parseDay)
      if False == r:
        continue
      ret['idList'].append(r)
    except Exception, e:
      # print repr(e)
      pass
  return ret


# 开盘价买入
def trace(id,parseDay):
  parser = PenetrateUpwardMa20Parser.PenetrateUpwardMa20Parser(parseDay)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,20)  # 最长持股时间不太可能超过20
  inDay = dayList[0]

  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为信号日第二天的开盘价
  slp = parser.getMinPriceOfDay(res,inDay)  # 初始止损价为买入当天的最低价
  
  outPrice = 0

  dayList = dayList[1:] # 去掉买入日
  for d in dayList: # 从第2天开始
    minPrice = parser.getMinPriceOfDay(res,d)

    if minPrice < slp: # 触发止损  要有大盘配合
      outPrice = slp
      break
    
    # 未止损的情况下，将止损位上调为当日最低价
    slp = minPrice


  if 0==inPrice:
    return False # 不可参与

  if 0==outPrice:
    return False

  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outPrice'] = outPrice
  return ret


# 回踩3日线买入
# def trace1(id,parseDay):
#   print id,parseDay
#   parser = PenetrateUpwardMa20Parser.PenetrateUpwardMa20Parser(parseDay)
#   priceFile = Tools.getPriceDirPath()+'/'+str(id)
#   res = open(priceFile,'r').read()
  
#   dayList = parser.getNextTradingDayList(parseDay,2)
#   inDay = dayList[0]
#   outDay = dayList[1]

#   endPriceOfParseDay = parser.getEndPriceOfDay(res,parseDay)
#   minPrice = parser.getMinPriceOfDay(res,inDay)  # 买入价为连板后第一天的最低价，且低于“回踩3日线”
#   outPrice = parser.getStartPriceOfDay(res,outDay)  # 卖出价为买入后第二天的开盘价

#   if 0==endPriceOfParseDay or 0==minPrice or 0==outPrice:
#     return False

#   orderPrice = endPriceOfParseDay*0.955
#   if orderPrice < minPrice:  # 预约价在最小价之下
#     return False  # 不可参与

#   # inDayStartPrice = parser.getStartPriceOfDay(res,inDay)
#   # startPriceGr = (inDayStartPrice - endPriceOfParseDay)/endPriceOfParseDay
#   # if startPriceGr > 0.07:  # 高开低走的，撤单
#   #   return False

#   inPrice = orderPrice # 

#   ret = {}
#   ret['id'] = id
#   ret['name'] = Tools.getNameById(id)
#   ret['inPrice'] = inPrice
#   ret['outPrice'] = outPrice
#   return ret



if __name__ == '__main__':
  # 跟踪所有中选股
  enterListFileList = getEnterListFiles()
  ret = []
  
  parsedNum = 0
  total = len(enterListFileList)
  for f in enterListFileList:
    printProcess(parsedNum,total)
    r = traceEnterList(f)
    ret.append(r)
    parsedNum += 1
  
  path = Tools.getTracerDirPath()+'/trace_report.data'
  open(path,'w').write(str(ret))


