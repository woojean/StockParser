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
from parsers import UpWardLimitParser


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
  ret = []
  parser = f.split('/')[-1][11:-4]
  parseDay = f.split('/')[-1][:10]
  idList = open(f,'r').read().split(',')

  for id in idList:
    try:
      r = trace(id,parseDay)
      if False == r:
        continue
      ret.append(r)
    except Exception, e:
      print repr(e)
      pass
  return ret


def trace(id,parseDay):
  parser = BaseParser.BaseParser(parseDay)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,1)
  nextDay = dayList[0]

  basePrice = parser.getEndPriceOfDay(res,parseDay)
  startPrice = parser.getStartPriceOfDay(res,nextDay)
  endPrice = parser.getEndPriceOfDay(res,nextDay)
  minPrice = parser.getMinPriceOfDay(res,nextDay)
  maxPrice = parser.getMaxPriceOfDay(res,nextDay)
  
  # print startPrice,endPrice,minPrice,maxPrice
  if 0==startPrice or 0==endPrice or 0==minPrice or 0==maxPrice:
    return {}

  ret = {}
  ret['id'] = id
  ret['parseDay'] = parseDay
  ret['basePrice'] = basePrice
  ret['startPrice'] = startPrice
  ret['endPrice'] = endPrice
  ret['minPrice'] = minPrice
  ret['maxPrice'] = maxPrice
  return ret


def getCountKey(rate):
  if -10 <= rate < -9:
    return '-10_-9'
  if -9 <= rate < -8:
    return '-9_-8'
  if -8 <= rate < -7:
    return '-8_-7'
  if -7 <= rate < -6:
    return '-7_-6'
  if -6 <= rate < -5:
    return '-6_-5'
  if -5 <= rate < -4:
    return '-5_-4'
  if -4 <= rate < -3:
    return '-4_-3'
  if -3 <= rate < -2:
    return '-3_-2'
  if -2 <= rate < -1:
    return '-2_-1'
  if -1 <= rate < 0:
    return '-1_0'
  if 0 <= rate < 1:
    return '0_1'
  if 1 <= rate < 2:
    return '1_2'
  if 2 <= rate < 3:
    return '2_3'
  if 3 <= rate < 4:
    return '3_4'
  if 4 <= rate < 5:
    return '4_5'
  if 5 <= rate < 6:
    return '5_6'
  if 6 <= rate < 7:
    return '6_7'
  if 7 <= rate < 8:
    return '7_8'
  if 8 <= rate < 9:
    return '8_9'
  if 9 <= rate < 10:
    return '9_10'
  


def count(data):
  ret = {
    'startPriceRate':{
      '-10_-9':0,
      '-9_-8':0,
      '-8_-7':0,
      '-7_-6':0,
      '-6_-5':0,
      '-5_-4':0,
      '-4_-3':0,
      '-3_-2':0,
      '-2_-1':0,
      '-1_0':0,
      '0_1':0,
      '1_2':0,
      '2_3':0,
      '3_4':0,
      '4_5':0,
      '5_6':0,
      '6_7':0,
      '7_8':0,
      '8_9':0,
      '9_10':0
    },
    'endPriceRate':{
      '-10_-9':0,
      '-9_-8':0,
      '-8_-7':0,
      '-7_-6':0,
      '-6_-5':0,
      '-5_-4':0,
      '-4_-3':0,
      '-3_-2':0,
      '-2_-1':0,
      '-1_0':0,
      '0_1':0,
      '1_2':0,
      '2_3':0,
      '3_4':0,
      '4_5':0,
      '5_6':0,
      '6_7':0,
      '7_8':0,
      '8_9':0,
      '9_10':0
    },
    'maxPriceRate':{
      '-10_-9':0,
      '-9_-8':0,
      '-8_-7':0,
      '-7_-6':0,
      '-6_-5':0,
      '-5_-4':0,
      '-4_-3':0,
      '-3_-2':0,
      '-2_-1':0,
      '-1_0':0,
      '0_1':0,
      '1_2':0,
      '2_3':0,
      '3_4':0,
      '4_5':0,
      '5_6':0,
      '6_7':0,
      '7_8':0,
      '8_9':0,
      '9_10':0
    },
    'minPriceRate':{
      '-10_-9':0,
      '-9_-8':0,
      '-8_-7':0,
      '-7_-6':0,
      '-6_-5':0,
      '-5_-4':0,
      '-4_-3':0,
      '-3_-2':0,
      '-2_-1':0,
      '-1_0':0,
      '0_1':0,
      '1_2':0,
      '2_3':0,
      '3_4':0,
      '4_5':0,
      '5_6':0,
      '6_7':0,
      '7_8':0,
      '8_9':0,
      '9_10':0
    },
    'indayRateRate':{
      '-10_-9':0,
      '-9_-8':0,
      '-8_-7':0,
      '-7_-6':0,
      '-6_-5':0,
      '-5_-4':0,
      '-4_-3':0,
      '-3_-2':0,
      '-2_-1':0,
      '-1_0':0,
      '0_1':0,
      '1_2':0,
      '2_3':0,
      '3_4':0,
      '4_5':0,
      '5_6':0,
      '6_7':0,
      '7_8':0,
      '8_9':0,
      '9_10':0
    },
  }
  for l in data:
    for item in l:
      if not item.has_key('startPrice'):
        continue
      startPrice = float(item['startPrice'])
      endPrice = float(item['endPrice'])
      maxPrice = float(item['maxPrice'])
      minPrice = float(item['minPrice'])
      basePrice = float(item['basePrice'])

      startPriceRate = 100.0*round((startPrice-basePrice)/basePrice,5)
      endPriceRate = 100.0*round((endPrice-basePrice)/basePrice,5)
      maxPriceRate = 100.0*round((maxPrice-basePrice)/basePrice,5)
      minPriceRate = 100.0*round((minPrice-basePrice)/basePrice,5)
      indayRateRate = 100.0*round((endPrice-startPrice)/startPrice,5)
      
      startPriceRateKey = getCountKey(startPriceRate)
      endPriceRateKey = getCountKey(endPriceRate)
      maxPriceRateKey = getCountKey(maxPriceRate)
      minPriceRateKey = getCountKey(minPriceRate)
      indayRateRateKey = getCountKey(indayRateRate)

      if startPriceRateKey==None\
        or endPriceRateKey==None\
        or maxPriceRateKey==None\
        or minPriceRateKey==None\
        or indayRateRateKey==None:
        continue

      ret['startPriceRate'][startPriceRateKey] +=1
      ret['endPriceRate'][endPriceRateKey] +=1
      ret['maxPriceRate'][maxPriceRateKey] +=1
      ret['minPriceRate'][minPriceRateKey] +=1
      ret['indayRateRate'][indayRateRateKey] +=1
  return ret


def dumpReport(countRet):
  rateList = ['-10_-9','-9_-8','-8_-7','-7_-6','-6_-5','-5_-4','-4_-3','-3_-2','-2_-1','-1_0','0_1','1_2','2_3','3_4','4_5','5_6','6_7','7_8','8_9','9_10']
  s = '<html>'
  s += '<head></head>'
  s += '<body>'
  s += '<table>'
  s += '<tr><td></td><td>startPriceRate</td><td>endPriceRate</td><td>maxPriceRate</td><td>minPriceRate</td><td>indayRateRate</td></tr>'
  for r in rateList:
    s += '<tr>'
    s += '<td>' + r + '</td>'
    s += '<td>' + str(countRet['startPriceRate'][r]) + '</td>'
    s += '<td>' + str(countRet['endPriceRate'][r]) + '</td>'
    s += '<td>' + str(countRet['maxPriceRate'][r]) + '</td>'
    s += '<td>' + str(countRet['minPriceRate'][r]) + '</td>'
    s += '<td>' + str(countRet['indayRateRate'][r]) + '</td>'
    s += '</tr>'
  s += '</table>'
  path = Tools.getReportDirPath()+'/UpWardLimitParser.count-report.html'
  open(path,'w').write(s)
  os.system('open '+path)


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
  
  path = Tools.getTracerDirPath()+'/UpWardLimitParser.count.data'
  open(path,'w').write(str(ret))
 
  countRet = count(ret)
  print countRet
  
  dumpReport(countRet)









