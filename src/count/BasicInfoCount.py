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


PE_RANGES = [
  ['< 10',0,10],
  ['10 ~ 20',10,20],
  ['20 ~ 30',20,30],
  ['30 ~ 40',30,40],
  ['40 ~ 50',40,50],
  ['50 ~ 60',50,60],
  ['60 ~ 70',60,70],
  ['70 ~ 80',70,80],
  ['80 ~ 90',80,90],
  ['90 ~ 100',90,100],
  ['>= 100',100,100000],
]


PB_RANGES = [
  ['< 1',0,1],
  ['1 ~ 2',1,2],
  ['2 ~ 3',2,3],
  ['3 ~ 4',3,4],
  ['4 ~ 5',4,5],
  ['5 ~ 6',5,6],
  ['6 ~ 7',6,7],
  ['7 ~ 8',7,8],
  ['8 ~ 9',8,9],
  ['9 ~ 10',9,10],
  ['>= 10',10,100000],
]

CR_RANGES = [
  ['0% ~ 0.1%',0,0.1],
  ['0.1% ~ 0.2%',0.1,0.2],
  ['0.2% ~ 0.3%',0.2,0.3],
  ['0.3% ~ 0.4%',0.3,0.4],
  ['0.4% ~ 0.5%',0.4,0.5],
  ['0.5% ~ 0.6%',0.5,0.6],
  ['0.6% ~ 0.7%',0.6,0.7],
  ['0.7% ~ 0.8%',0.7,0.8],
  ['0.8% ~ 0.9%',0.8,0.9],
  ['0.9% ~ 1%',0.9,1],
  ['1% ~ 1.1%',1,1.1],
  ['1.1% ~ 1.2%',1.1,1.2],
  ['1.2% ~ 1.3%',1.2,1.3],
  ['1.3% ~ 1.4%',1.3,1.4],
  ['1.4% ~ 1.5%',1.4,1.5],
  ['1.5% ~ 1.6%',1.5,1.6],
  ['1.6% ~ 1.7%',1.6,1.7],
  ['1.7% ~ 1.8%',1.7,1.8],
  ['1.8% ~ 1.9%',1.8,1.9],
  ['1.9% ~ 2%',1.9,2],
  ['2% ~ 3%',2,3],
  ['3% ~ 4%',3,4],
  ['4% ~ 5%',4,5],
  ['5% ~ 6%',5,6],
  ['6% ~ 7%',6,7],
  ['7% ~ 8%',7,8],
  ['8% ~ 9%',8,9],
  ['9% ~ 10%',9,10],
  ['>= 10%',10,100000],
]


def dump(csvPe,csvPb,csvCr):
  s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head>'
  s +='<body>'
  

  # --- PE
  s += '<h3>市盈率</h3>'
  s += '<hr/>'
  s += '<table width="40%" border="0"  cellspacing="0" cellpadding="0" style="word-break:break-all;word-wrap:break-word">'
  s +='<tr style="font-size:1.2em"><td>范围</td><td>数量</td><td>占比</td></tr>'

  sumOfNum = 0
  for k,v in csvPb.items():
    sumOfNum += v

  for rg in PE_RANGES:
    num = csvPe[rg[0]]
    per = round(num*100.0/sumOfNum,3)
    
    style = '"color:black;"'
    if per >=10:
      style = '"color:red;"'

    s += '<tr style='+style+'>'
    s +='<td>' + rg[0] + '</td>'
    s +='<td>' + str(num) + '</td>'
    s +='<td>' + str(per) + ' %</td>'
    s +='</tr>'
  s += '</table>'
  s += '<br/>'

  # --- PB
  s += '<h3>市净率</h3>'
  s += '<hr/>'
  s += '<table width="40%" border="0"  cellspacing="0" cellpadding="0" style="word-break:break-all;word-wrap:break-word">'
  s +='<tr style="font-size:1.2em"><td>范围</td><td>数量</td><td>占比</td></tr>'

  sumOfNum = 0
  for k,v in csvPe.items():
    sumOfNum += v

  for rg in PB_RANGES:
    num = csvPb[rg[0]]
    per = round(num*100.0/sumOfNum,3)

    style = '"color:black;"'
    if per >=10:
      style = '"color:red;"'

    s += '<tr style='+style+'>'
    s +='<td>' + rg[0] + '</td>'

    s +='<td>' + str(num) + '</td>'

    per = round(num*100.0/sumOfNum,3)
    s +='<td>' + str(per) + ' %</td>'
    s +='</tr>'
  s += '</table>'
  s += '<br/>'

  # --- CR
  s += '<h3>换手率</h3>'
  s += '<hr/>'
  s += '<table width="40%" border="0"  cellspacing="0" cellpadding="0" style="word-break:break-all;word-wrap:break-word">'
  s +='<tr style="font-size:1.2em"><td>范围</td><td>数量</td><td>占比</td></tr>'

  sumOfNum = 0
  for k,v in csvCr.items():
    sumOfNum += v

  for rg in CR_RANGES:
    num = csvCr[rg[0]]
    per = round(num*100.0/sumOfNum,3)

    style = '"color:black;"'
    if per >= 5:
      style = '"color:red;"'

    s += '<tr style='+style+'>'
    s +='<td>' + rg[0] + '</td>'
    s +='<td>' + str(num) + '</td>'
    s +='<td>' + str(per) + ' %</td>'
    s +='</tr>'
  s += '</table>'


  s +='</body>'
  s +='</html>'
  path = Tools.getReportDirPath()+'/pe_pb.html'
  open(path,'w').write(s)


if __name__ == '__main__':
  path = Tools.getBasicDirPath()

  csvPe = {}
  csvPb = {}
  csvCr = {}
  for root,dirs,files in os.walk(path):
      for f in files:
        try:
          if len(f) == 6:
            id = f
            info = BaseParser.BaseParser.getBasicInfoById(id)
            pe = float(info[38])
            pb = float(info[43])
            cr = float(info[37])

            # PE
            for rg in PE_RANGES:
              k = rg[0]
              if pe >= rg[1] and pe < rg[2]:
                if not csvPe.has_key(k):
              	  csvPe[k] = 1
                else:
              	  csvPe[k] += 1

            # PB
            for rg in PB_RANGES:
              k = rg[0]
              if pb >= rg[1] and pb < rg[2]:
                if not csvPb.has_key(k):
              	  csvPb[k] = 1
                else:
              	  csvPb[k] += 1

            # CR
            for rg in CR_RANGES:
              k = rg[0]
              if cr >= rg[1] and cr < rg[2]:
                if not csvCr.has_key(k):
              	  csvCr[k] = 1
                else:
              	  csvCr[k] += 1

        except Exception, e:
          pass
          #print repr(e)

  print csvPe
  print csvPb
  print csvCr

  dump(csvPe,csvPb,csvCr)



