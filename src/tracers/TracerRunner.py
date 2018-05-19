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
  # config ==========================================================================
  parserList = [
    'BaldRiseLineAndVolumeReduceParser',
    #'ContinuouslyBigRiseButNoRiseLimitParser',
    #'GoldenPinBottomParser',
    #'MacdReverseParser',
    #'MaConvergenceParser',
    #'MaPenetrateParser',
    #'MaTrendParser',
    #'MaxPriceParser',
    #'OneLimitsParser',
    #'PenetrateUpwardMa60Parser',
    #'RgbParser',
    #'StandOn60Parser',
    #'SwallowUpParser',
    #'ThreeLimitsParser',
    #'TriangularSupportParser',
    #'TwoLimitsParser',
    #'VenusParser',
    #'VolumeMutationParser',
    #'WJParser',
    #'PriceAndVolumeParser'
  ]


  beginDate = '2016-08-17'
  traceDays = 400 # 统计天数

  isNew = False if (len(sys.argv) <= 1) else ('new' ==sys.argv[1])
  if isNew:
    Tools.initDir('enterList')

    for parser in parserList:
      # run parser ======================================================================
      print parser,beginDate,traceDays
      dayList = BaseParser.BaseParser.getNextTradingDayList(beginDate,traceDays-1)
      dayList.insert(0,beginDate)
      print dayList

      for parseDay in dayList:
        print parseDay
        cmd = 'python '+Tools.getParsersDirPath() + '/'+ parser +'.py ' + parseDay
        print cmd
        os.system(cmd)

  cmd = 'python '+Tools.getTracersDirPath() + '/WJTracer.py'
  os.system(cmd)
  
  cmd = 'python '+Tools.getTracersDirPath() + '/TracerReport.py'
  os.system(cmd)


   













