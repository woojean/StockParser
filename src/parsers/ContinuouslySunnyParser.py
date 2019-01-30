#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-11
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
连阳
'''
class ContinuouslySunnyParser(BaseParser):
  _tag = 'ContinuouslySunnyParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def parse(self,res,parseDay,id=''):
    if not self.isContinuouslySunny(res,parseDay,5,True):
      return False

    return True


if __name__ == '__main__':
  print 'ContinuouslySunnyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = ContinuouslySunnyParser(parseDay).getParseResult(True)
  print idList

















