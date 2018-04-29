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



if __name__ == '__main__':
  # config ==========================================================================
  parserList = [
    #'BaldRiseLineAndVolumeReduceParser',
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
    'WJParser'
  ]

  # 2017-01-17 - 2017-05-05
  beginDate = '2017-01-17'
  countNum = 71 # 统计天数
  traceNum = 1  # 跟踪天数


  Tools.initDir('count')

  for parser in parserList:
    # run parser ======================================================================
    Tools.initDir('enterList')

    print parser,beginDate,countNum,traceNum
    dayList = BaseParser.BaseParser.getNextTradingDayList(beginDate,countNum)
    print dayList

    for parseDay in dayList:
      print parseDay
      cmd = 'python '+Tools.getParsersDirPath() + '/'+ parser +'.py ' + parseDay
      print cmd
      os.system(cmd)
  

    # count ===========================================================================
    selectedList = {}
    enterListDirPath = Tools.getEnterListDirPath()
    for root,dirs,files in os.walk(enterListDirPath):
      for f in files:
        try:
          path = root + '/' + f
          date = f[:10]
          idList = open(path,'r').read().split(',')
          if len(idList)<2:  # 会包含''
            continue
          selectedList[date] = idList
        except Exception, e:
          pass
          print repr(e)
  
    print selectedList
  

    # trace ===========================================================================
    selectedNum = 0
    riseNum = 0
    declineNum = 0
    drawNum = 0

    totalRise = 0.0
    avgRise = 0.0
    for parseDay,idList in selectedList.items():
      try:
        dayList = BaseParser.BaseParser.getNextTradingDayList(parseDay,traceNum)
        traceDay = dayList[-1]
        for id in idList:
          selectedNum += 1
          growthRate = BaseParser.BaseParser(parseDay).getGrowthRate(id,parseDay,traceDay)
          totalRise += growthRate
          if growthRate > 0:
            riseNum +=1
          elif growthRate == 0:
            drawNum += 1
          elif growthRate < 0:
            declineNum += 1
      except Exception, e:
        pass
        #print repr(e)
    avgRise = round(totalRise/selectedNum,3)

    print 'selectedNum: '+ str(selectedNum)
    print 'riseNum: '+ str(riseNum)
    print 'declineNum: '+ str(declineNum)
    print 'drawNum: '+ str(drawNum)
    print 'avgRise: '+ str(avgRise)+'%'


    # dump ============================================================================
    s = str(selectedNum)
    s += ','+str(riseNum)
    s += ','+str(declineNum)
    s += ','+str(drawNum)
    s += ','+str(avgRise)+'%'

    path = Tools.getCountDirPath() + '/' + parser +'-' + beginDate + '-' +  str(countNum) +'-' + str(traceNum) 
    open(path,'w').write(s)















