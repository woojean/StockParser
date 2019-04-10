#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-12-20
'''

import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime
from BaseParser import BaseParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
'''
class UpParser(BaseParser):
  _tag = 'UpParser'

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def calcuR(self,idList,num):
    num = 50
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      gr = self.getGrOfDays(res,parseDay,60)

      vList.append((id,gr))

    # 排序
    sList = sorted(vList,key=lambda x: -x[1]) 
    # sList = sorted(vList,key=lambda x: x[1]) 
    print "sorted list:"
    print sList
    selectedList = sList[:num]

    print "\nselected list:"
    print selectedList
    l = []
    for item in selectedList:
      l.append(item[0])
    return l


  def parse(self,res,parseDay,id=''):
    # gr = self.getGrOfDays(res,parseDay,60)
    # if gr < 0.2:
    #   return False

    return True





if __name__ == '__main__':
  print 'UpParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = UpParser(parseDay).getParseResult(True)
  print idList

















