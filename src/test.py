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
  res = '03","2018-03-30,33.70,33.29,33.99,33.17,572692,19.2亿,2.4%,0.59","20]})'
  p = '"'+ day +',(.*?)%"'
  print p
  ret = re.findall('"'+ day +',(.*?)%"', res)
  #ret = re.findall('"2018-03-30,(.*?)%', res)
  #                  "2018-03-30,(.*?)%"
  print ret