#coding:utf-8
#!/usr/bin/env python

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


class MuThreadDemo(threading.Thread): 
  _idList = []   # 本次线程需要处理的任务
  _threadId = 0  # 本次线程的ID

  def __init__(self,idList=[],threadId=0): 
    self._idList = idList
    self._threadId = threadId
    threading.Thread.__init__(self) 

  def run(self):
    for id in self._idList:
      try:
        # doing
        # ...
        print str(self._threadId) +' -> ' +str(id)
        time.sleep(1) # 休眠1秒
      except:
        pass


if __name__ == '__main__':
  print 'MuThreadDemo'

  threads = 3 # 线程数（不能少于任务数）
  idList = [1,2,3,4,5,6,7,8,9,10]

  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    demo = MuThreadDemo(subIdList,threadId)
    demo.start()




