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

'''
'''

def getMonitorIdList():
  dirPath = Tools.getMonitorDirPath()
  idList = []
  for root,dirs,files in os.walk(dirPath):
    for f in files:
      try:
        if len(f) == 6:
          id = f
          idList.append(id)
      except Exception, e:
        pass
        print repr(e)
  return idList


def genIdListFile(idList):
  s = ','.join(idList)
  enterListDirPath = Tools.getEnterListDirPath()
  open(enterListDirPath + '/monitor.sel','w').write(s)

	

if __name__ == '__main__':
  idList = getMonitorIdList()
  print idList
  print "\n================================================\n"
  print "总数："+ str(len(idList))
  genIdListFile(idList)
