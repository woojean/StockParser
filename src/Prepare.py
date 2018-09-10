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

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools


if __name__ == '__main__':

  cmd = 'python '+Tools.getSpiderDirPath() + '/PriceSpider.py new'
  print cmd
  os.system(cmd)

  cmd = 'python '+Tools.getSpiderDirPath() + '/BasicInfoSpider.py new'
  print cmd
  os.system(cmd)
  
















