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
    'BaldRiseLineAndVolumeReduceParser':'光头光脚阳线且缩量',
    'RgbParser':'短线均线多头',
    'MaxPriceParser':'新高',
    'GoldenPinBottomParser':'“金针探底”',
    'VenusParser':'启明星',
    'SwallowUpParser':'向上吞没线',
    'VolumeMutationParser':'成交量突变',
    'MacdReverseParser':'MACD趋势反转'
  }
  
  xq = ''
  dirEnterList = Tools.getEnterListDirPath()
  xq += '<b>盘后技术选股（'+parseDay+'）'+'</b> \n'
  xq += '分析工具的源代码见这里：https://github.com/woojean/StockParser'
  for parser,tag in parsers.items():
    try:
      f = dirEnterList+'/'+parseDay+'-'+parser+'.sel'
      l = open(f,'r').read().split(',')
      
      xq += "\n"
      xq += "\n"
      xq += '<b>' + tag + '</b> （'+str(len(l))+'）'
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








