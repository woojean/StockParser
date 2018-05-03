#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-06
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

'''
涨幅 + 换手率
'''
class PriceAndVolumeParser(BaseParser):
  _tag = 'PriceAndVolumeParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 



  def parse(self,res,parseDay,id=''):
    amplitude = self.getAmplitudeOfDay(res,parseDay)
    changeRate = self.geChangeRateOfDay(res,parseDay)
    if amplitude > 0.04:
      return False
    #if changeRate < 0.2:
    #  return False
    return True


if __name__ == '__main__':
  print 'PriceAndVolumeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = PriceAndVolumeParser(parseDay).getParseResult(True)
  print idList

















