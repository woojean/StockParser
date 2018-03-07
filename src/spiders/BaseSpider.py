#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-06
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

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

if __name__ == '__main__':
  print rootPath

class BaseSpider(threading.Thread): 
  _idList = []   # 本次线程需要处理的任务
  _threadId = 0  # 本次线程的ID
  _dataPath = ''
  _failedDataPath = ''
  _source = ''

  def __init__(self,idList=[],threadId=0): 
    self._idList = idList
    self._threadId = threadId
    self._dataPath = self._source
    self._failedDataPath = 'failed_' + self._source
    threading.Thread.__init__(self) 

  def getRootPath(self):
    return Tools.getRootPath()
  
  def initDir(self):
    if len(self._source) < 1:
      raise Exception("Exception：source未设置！")
    if BaseSpider.isNew():
      Tools.initDir(self._source)
      Tools.initDir('failed_' + self._source)
    else:
      Tools.touchDir(self._source)
      Tools.touchDir('failed_' + self._source)

  @staticmethod
  def getIdList():
    return Tools.getIdList()

  @staticmethod
  def isNew():
    isNew = False if (len(sys.argv) <= 1) else ('new' ==sys.argv[1])
    return isNew

  def dumpFile(self,id,data):
    path = (self.getRootPath()+'/data/'+self._failedDataPath+'/') if (len(data) < 100) else (self.getRootPath()+'/data/'+self._dataPath+'/')
    f = open(path+id,'w')
    f.write(data)
    f.close()

  def isDataSuccess(self,id):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'+id
    return os.path.exists(path)
  
  def setParams(self,idList,threadId):
    self._idList = idList
    self._threadId = threadId

  def run(self):
    for id in self._idList:
      idType = str(id)[0]
      if idType not in ['6','0']: # 只看A股 0 深，6 沪，3 创业板，5 基金权证， 1 深市基金
        continue

      try:
        if self.isDataSuccess(id):
          continue
        url = self.genUrl(id)
        print str(self._threadId) + ' -> ' +str(id)
        data = requests.get(url,verify=False).text
        self.dumpFile(id,data)
      except:
        #print 'Exception:'+i
        pass



if __name__ == '__main__':
  print 'BaseSpider'




