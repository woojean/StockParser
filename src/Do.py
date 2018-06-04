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
from parsers import BaseParser


NUM_ICON = {
  1:'①',
  2:'②',
  3:'③',
  4:'④',
  5:'⑤',
  6:'⑥',
  7:'⑦',
  8:'⑧',
  9:'⑨',
  10:'⑩'
}

def getParams():
  parseDay = time.strftime('%Y-%m-%d',time.localtime(time.time())) if (len(sys.argv) <= 1) else sys.argv[1]
  isNew = False if (len(sys.argv) <= 2) else ('new' ==sys.argv[2])
  traceDay = '' if (len(sys.argv) <= 3) else sys.argv[3]
  return (parseDay, isNew,traceDay)

def getLinkById(id):
  link = '#'
  if(id[0] == '0'):
  	link = 'http://quote.eastmoney.com/sz'+id+'.html'
  elif(id[0] == '6'):
  	link = 'http://quote.eastmoney.com/sh'+id+'.html'
  return link

def runSpiders(spiders):
  for spider in spiders:
    cmd = 'python '+Tools.getSpiderDirPath() + '/'+spider+'.py new'
    print cmd
    os.system(cmd)


  
def report(parseDay,parsers,isOpen=False,traceDay=''):
  sel = ''
  s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
  s += '''
<style>
a:link    { color:blue; }
a:visited { color:blue; }
a:hover   { color:red; }
a:active  { color:yellow; }

font-size:0.8em;

td{
  font-size:0.8em;
}
</style>
  '''
  s += '</head><body>'
  
  focusTotal = 0
  focusRise = 0
  nums = {}
  riseNums = {}
  count = {} # for font size
  tb = '<tr valign="top" align="center">'
  dirEnterList = Tools.getEnterListDirPath()
  for parser,tag in parsers.items():
    riseNums[parser] = 0
    nums[parser] = 0
    try:
      f = dirEnterList+'/'+parseDay+'-'+parser+'.sel'
      l = open(f,'r').read().split(',')
      nums[parser] = len(l)
      if len(l[0]) < 1: # 可能解析出来是空字符
        nums[parser] = 0 

      tb += '<td style="border:1px solid #eee;"><br/>'

      if len(l) > 100: # 太多，无意义
        tb += '失真（选股过多）'
        tb += '<br/><br/>'
        continue

      for id in l: 
        try:
          if count.has_key(id):
            count[id] += 1
          else:
            count[id] = 1
          name = Tools.getNameById(id)
          link = getLinkById(id)
          
        
          div = '<div $_style_$>'

          # trace
          color = 'black'
          traceDayGrowthRate = 0
          if len(traceDay) == 10:
            traceDayGrowthRate = BaseParser.BaseParser(parseDay).getGrowthRate(id,parseDay,traceDay)
            if not riseNums.has_key(parser):
              riseNums[parser] = 0
            if traceDayGrowthRate > 0:
              color = 'red'
              riseNums[parser] +=1
            elif traceDayGrowthRate < 0:
              color = 'green'
            div +='<font size=1 color="' + color + '">' + str(round(traceDayGrowthRate,3)) + ' %</font></br>'

          countNum = ''
          if count[id] > 1:
            countNum = '<font size=1>'+NUM_ICON[count[id]]+'</font>'

          # id
          div +='<a href="'+link+'" target="_blank">'
          div +='<font size='+ str(count[id]) +'>' + str(id) + '</font>'
          div +='</a></br>'

          # name
          div +='<font size='+ str(count[id]) +'  color="' + color + '"><b>' + name +' '+ countNum+ '</b></font>'

          isFocus = True
          
          # RGB
          isRgb = BaseParser.BaseParser(parseDay).isRgb(id,parseDay)
          if isRgb:
            div += '<br/>'
            div += '<font size=2 color="red"><b>↗</b></font>' 
            div += '<font size=2 color="green"><b>↗</b></font>' 
            div += '<font size=2 color="blue"><b>↗</b></font>' 
          else:
            isFocus = False

          # CR
          basicInfo = BaseParser.BaseParser.getBasicInfoById(id)
          changeRate = float(basicInfo[37])
          if changeRate >= 3.0:
            div += '<br/><font size=1 color="orange">换手率： '+str(changeRate)+'% </font>' 
          else:
            isFocus = False
          
          # Focus
          if isFocus:
            div = div.replace('$_style_$','style="border:1px dashed #F00;border-radius:10px;width:80%;";')
            sel += str(id)+','
            focusTotal +=1
            if len(traceDay) == 10:
              if traceDayGrowthRate > 0:
                focusRise +=1


          div +='</div><br/><br/>'
          tb += div
        except Exception, e:
          pass
          #print repr(e)
      tb +='</td>'
    except Exception, e:
      pass
      #print repr(e)
  tb += '</tr>'


  # TH
  w = str(100/len(parsers))+'%'
  th = '<tr align="center">'
  for parser,tag in parsers.items():
    try:
      riseNum = ''
      if len(traceDay) == 10:
        riseNum = '<font color="red">'+str(riseNums[parser])+'</font>/'
      th += '<td width="'+ w +'" style="border:1px solid #000;padding:10px;">'
      th += '<font color="red">'+tag +'</font>'+'<br/>'+riseNum+'<font color="black" size=1>[ <b>'+str(nums[parser])+'</b> ]</font>'
      th +='</td>'
    except Exception, e:
      pass
      #print repr(e)
  th += '</tr>'

  # sum
  total = 0
  for k,v in nums.items():
    total += int(v)
  s += '<table width="100%"><tr>'
  s +='<td align="left"><font color="red"><b>盘后技术选股（'+parseDay +'）</b></font></td>'
  if len(traceDay) == 10:
    s +='<td align="left">Trace Day: '+traceDay +'</td>'
  s +='<td align="right">'+' Total: <font color="red"> '+str(total)+'</font>'+'</td>'
  s +='</tr></table>'
  s += '<hr/>'
  

  if len(traceDay) == 10:
    s += '<div>Focus Rise Rate: <font size=3 color="red">'+str(focusRise) + '</font>/' +str(focusTotal) +'</div><br/>'


  s += '<table width="100%" border="0"  cellspacing="0" cellpadding="0" style="word-break:break-all;word-wrap:break-word">'
  s += th
  s += tb
  s += '</body></html>'
  path = Tools.getReportDirPath()+'/'+parseDay+'.html'
  open(path,'w').write(s)

  selPath = Tools.getReportDirPath()+'/'+parseDay+'.sel'
  open(selPath,'w').write(sel[:-1])

  if isOpen:
  	os.system('open '+path)



def run(parseDay,parsers,isNew=False):
  if isNew:
    spiders = [
      'PriceSpider',
      'MacdSpider',
      'BasicInfoSpider'
    ]
    runSpiders(spiders)
    
  Tools.initDir('enterList')
  for parser,tag in parsers.items():
    cmd = 'python '+Tools.getParsersDirPath() + '/'+ parser +'.py ' + parseDay
    print cmd
    os.system(cmd)

    
'''
python src/Do.py 2018-03-26 x 2018-04-09 
'''

if __name__ == '__main__':


  parsers = {
    'BaldRiseLineAndVolumeReduceParser':'秃阳线且缩量☆',
    # 'ContinuouslyBigRiseButNoRiseLimitParser':'连续大涨',
    # 'FlatBottomParser':'平台',
    'GoldenPinBottomParser':'金针探底',
    # 'MacdReverseParser':'MACD反转☆',
    # 'MaConvergenceParser':'均线汇合',
    # 'MaPenetrateParser':'均线穿透',
    'MaTrendParser':'MA短线趋势',
    'MaxPriceParser':'创新高',
    'MergedParser.py':'均线汇合',
    'OneLimitsParser':'一板',
    'PenetrateUpwardMa60Parser':'上穿60日线',
    'RgbParser':'短线多头',
    'StandOn60Parser':'站稳60日均线',
    'SwallowUpParser':'向上吞没线',
    'ThreeLimitsParser':'三板',
    'TriangularSupportParser':'均线三角托',
    # 'TweezersBottomParser':'镊形底',
    'TwoLimitsParser':'二板',
    'VenusParser':'启明星',
    'VolumeMutationParser':'成交量突变',
    # 'WJParser':'WJ'
  }

  parsers2 = {
    'BaldRiseLineAndVolumeReduceParser':'秃阳线且缩量☆',  # BALD
    'TweezersBottomParser':'镊形底',  # TW
  }

  (parseDay, isNew,traceDay) = getParams()

  # ======================================================
  run(parseDay,parsers,isNew)
  report(parseDay,parsers,True,traceDay)



  
















