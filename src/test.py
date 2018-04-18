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



if __name__ == '__main__':
  pass
  day = '2018-03-30'
  res = '''
  0.95%,1.03","2018-03-30,33.70,33.29,33.99,33.17,572692,19.2亿,2.4%,0.59","2018-04-02,33.65,33.49,34.4
  '''
  p = '"'+ day +',(.*?)",'
  print p
  ret = re.findall(p, res)
  #ret = re.findall('"2018-03-30,(.*?)%', res)
  #                  "2018-03-30,(.*?)%"
  print ret