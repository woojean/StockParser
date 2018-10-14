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
from parsers import KdjParser


if __name__ == '__main__':
  pass
  parseDay = '2018-01-02'
  id = '000793'
  dStatus = KdjParser.KdjParser.isDBad(parseDay,id)
  print dStatus
