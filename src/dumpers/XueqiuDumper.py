#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-08
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser

if __name__ == '__main__':
  parseDay = time.strftime('%Y-%m-%d',time.localtime(time.time())) if (len(sys.argv) <= 1) else sys.argv[1]
  parsers = {
    'BaldRiseLineAndVolumeReduceParser':'秃阳线且缩量☆',
    'GoldenPinBottomParser':'金针探底',
    'MacdReverseParser':'MACD反转☆',
    'MaConvergenceParser':'均线汇合',
    'MaPenetrateParser':'均线穿透',
    'MaTrendParser':'MA短线趋势',
    'MaxPriceParser':'创新高',
    'OneLimitsParser':'一板',
    'RgbParser':'短线多头',
    'SimpleParser':'简单解析',
    'SwallowUpParser':'向上吞没线',
    'ThreeLimitsParser':'三板',
    'TriangularSupportParser':'均线三角托',
    'TwoLimitsParser':'二板',
    'VenusParser':'启明星',
    'VolumeMutationParser':'成交量突变',
  }

  parsers2 = {
    
    
  }

  xq = ''
  dirEnterList = Tools.getEnterListDirPath()
  xq += '<b>盘后技术选股（'+parseDay+'）'+'</b> \n'
  #xq += '分析工具的源代码见这里：https://github.com/woojean/StockParser'
  for parser,tag in parsers.items():
    print parser
    try:
      f = dirEnterList+'/'+parseDay+'-'+parser+'.sel'
      l = open(f,'r').read().split(',')
      
      xq += "\n"
      xq += "\n"
      xq += '<b>' + tag + '</b> （共：'+str(len(l))+'个）'
      xq += "\n"
      xq += "\n"

      c = 0
      for id in l:
        name = Tools.getNameById(id)
        if len(name) < 1:
          continue

        xq += name +' ('+str(id)+')'
        xq += " 、 "
        if c%4 == 0:
          xq += '\n'
        c += 1
    except Exception, e:
      print e
      pass
  
  path = Tools.getReportDirPath()+'/'+'XQ-'+parseDay+'.data'
  open(path,'w').write(xq)









