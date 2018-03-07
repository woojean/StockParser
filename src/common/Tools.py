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
 
reload(sys)
sys.setdefaultencoding('utf-8')

def getRootPath():
  rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
  return rootPath

def getParsersDirPath():
  return getRootPath()+'/src/parsers'  

def getBasicDirPath():
  return getRootPath()+'/data/basic'  

def getPriceDirPath():
  return getRootPath()+'/data/price'  # 价格数据的存储路径

def getSpiderDirPath():
  return getRootPath()+'/src/spiders'

def getReportDirPath():
  path = getRootPath()+'/data/report'  # 价格数据的存储路径
  if not os.path.exists(path):
    os.mkdir(path)
  return path

def getEnterListDirPath():
  dirPath =  getRootPath()+'/data/enterList'  
  if not os.path.exists(dirPath):
    os.mkdir(dirPath)

  return dirPath 

def getMacdDirPath():
  return getRootPath()+'/data/macd'


def getNameById(id):
  try:
    res = open(getRootPath()+'/data/price/'+str(id),'r').read()
    name = re.findall('"name":"(.*?)"', res)[0]
  except Exception, e:
    pass
    #print repr(e)
    name = '-'
  return str(name)

def getAllTradeDayList():
  s = open(getRootPath()+'/data/price/000001','r').read()
  idx = s.index('"data":[')
  s = s[idx:]
  allDayList = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", s)
  return allDayList


def initDir(dirName):
  print 'init data dir ...'
  dirPath = getRootPath()+'/data/'+dirName
  print dirPath

  if os.path.exists(dirPath):
    shutil.rmtree(dirPath)  

  print 'mkdir...'
  os.mkdir(dirPath)


def touchDir(dirName):
  print 'touch data dir ...'
  dirPath = getRootPath()+'/data/'+dirName
  print dirPath

  if not os.path.exists(dirPath):
    os.mkdir(dirPath) 


def getIdList():
  # http://quote.eastmoney.com/stocklist.html
  f = open(getRootPath()+'/config/allIdList','r')
  data = f.read()
  idList = re.findall('\((.*?)\)', data)

  f = open(getRootPath()+'/config/ignoreIdList','r')
  data = f.read()
  ignoreIdList = re.findall('\((.*?)\)', data)
  f.close()
  idList = [item for item in idList if item not in ignoreIdList]
  return idList














