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


def do(day,id):
  ret = [0,0]  # n,r
  ret[0] = 2
  ret[1] = 0.3
  return ret

if __name__ == '__main__':
  path = Tools.getEnterListDirPath()
  
  # 信号发出后第n天触及信号发出日最低价
  # 以及期间的最高价涨幅（相对信号发出日收盘价）
  N = []
  R = []
  for root,dirs,files in os.walk(path):
    for f in files:
      try:
        day = f[:10]
        idList = open(root+'/'+f,'r').read().split(',')
        for id in idList:
          ret = do(day,id)
          N.append(str(ret[0]))
          R.append(str(ret[1]))
      except Exception, e:
        pass
        #print repr(e)

    s = ','.join(N)
    path = Tools.getCountDirPath() + '/InitialStopLossCount.N.csv'  
    open(path,'w').write(s)

    s = ','.join(R)
    path = Tools.getCountDirPath() + '/InitialStopLossCount.R.csv'  
    open(path,'w').write(s)





