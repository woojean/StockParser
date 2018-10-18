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
import random

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser

class Runner(threading.Thread): 
  _dayList = []
  _threadId = 0  # 本次线程的ID

  def __init__(self,dayList=[],threadId=0): 
    self._dayList = dayList
    self._threadId = threadId
    threading.Thread.__init__(self) 

  def run(self):
    try:
      for parseDay in self._dayList:
        # print parseDay
        print str(self._threadId) + ' -> ' + parseDay
        cmd = 'python '+Tools.getParsersDirPath() + '/'+ parser +'.py ' + parseDay
        print cmd
        os.system(cmd)
    except Exception, e:
      pass
      print repr(e)


'''
'''

if __name__ == '__main__':
  # 回测parser
  parser = 'KdjParser'
  # parser = 'MaSupportParser'

  # 起止日期
  # 2018-06-20 24 2018-07-23 上证-0.08%
  # beginDate = '2016-08-31'  
  # testDays = 489
  
  # beginDate = '2018-01-02'  
  # testDays = 164
  # testDays = 183  # 9-28

  # beginDate = '2018-02-28'  
  beginDate = '2018-08-22'  
  testDays = 10


  dayList = BaseParser.BaseParser.getNextTradingDayList(beginDate,testDays-1)
  dayList.insert(0,beginDate)
  print dayList

  isNew = False if (len(sys.argv) <= 1) else ('new' ==sys.argv[1])
  if isNew:
    Tools.initDir('enterList')
  
  print parser,beginDate,testDays
  print dayList
  
  for parseDay in dayList:
    cmd = 'python '+Tools.getParsersDirPath() + '/'+ parser +'.py ' + parseDay
    print cmd
    os.system(cmd)
    

  '''
  threads = 32 # 线程数（不能少于任务数）
  step = len(dayList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subDayList = dayList[((threadId-1)*step):(threadId*step)]
    # runner = Runner(subDayList,threadId)
    # runner.start()
    print subDayList
  '''
    

  cmd = 'python '+ rootPath + '/src/back-test/Tester-'+parser+'.py'
  print cmd
  os.system(cmd)

  cmd = 'python '+ rootPath + '/src/back-test/Reporter-'+parser+'.py'
  print cmd
  os.system(cmd)



   













