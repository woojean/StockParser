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



if __name__ == '__main__':
  # 回测parser
  parser = 'PenetrateUpwardMa20Parser'

  # 起止日期
  # 2018-06-20 24 2018-07-23 上证-0.08%
  # beginDate = '2018-06-20'  
  # testDays = 20
  beginDate = '2018-01-02'  # 上证-16%+
  testDays = 150
  # beginDate = '2018-07-02'  
  # testDays = 1

  isNew = False if (len(sys.argv) <= 1) else ('new' ==sys.argv[1])
  if isNew:
    Tools.initDir('enterList')
    print parser,beginDate,testDays
    
    dayList = BaseParser.BaseParser.getNextTradingDayList(beginDate,testDays-1)
    dayList.insert(0,beginDate)
    print dayList

    for parseDay in dayList:
      print parseDay
      cmd = 'python '+Tools.getParsersDirPath() + '/'+ parser +'.py ' + parseDay
      print cmd
      os.system(cmd)

  cmd = 'python '+Tools.getBackTestDirPath() + '/Tester-'+parser+'.py'
  print cmd
  os.system(cmd)
  
  cmd = 'python '+Tools.getBackTestDirPath() + '/Reporter-'+parser+'.py'
  print cmd
  os.system(cmd)


   













