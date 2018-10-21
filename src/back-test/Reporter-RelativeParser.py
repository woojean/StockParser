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

'''
开始日期 结束日期 交易总数 赢利交易平均收益率 亏损交易平均亏损率 日均收益率 单笔交易平均收益率

买入日 代码 名称 买入价 卖出价 收益率
'''

if __name__ == '__main__':
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
  padding: 6px 6px 6px 12px;
  text-align: center;
}

table {
  width: 100%;
  padding-top: 20px;
  padding-bottom: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
  border: 1px;
  border-radius: 0.8em;
  cellspacing="0";
  border-collapse: collapse;
  border: 1px solid gold;
  background: #fff;
  color: #4f6b72;
  text-align: center;
}


.ah{
  font-weight:bold;
}

.ar{
  text-align: center;
  border: 1px solid gold;
}


.al{
  text-align: center;
  border-bottom: 1px dashed gold;
  border-right: 1px dashed gold;
}




</style>
  '''
  s += '</head><body>'

  # ================================================================================
  f = 'trace_report.data'
  p = Tools.getTracerDirPath()+'/'+f
  data = open(p,'r').read()
  data = eval(data)

  # ================================================================================
  beginDate = data[0]['parseDay'] 
  endDate = data[-1]['parseDay'] 
  
  totalDays = 0

  totalTradeNum = 0  # 交易总数
  totalGrowthRate = 0 # 总收益率（总盈利 + 总亏损）
  
  totalWinNum = 0 # 总赢利数
  totalWinRate = 0  # 总赢利

  totalLoseNum = 0 # 总亏损数
  totalLoseRate = 0  # 总亏损
  
  totalDayAvgGrowthRate = 0

  tables = ''
  for item in data: # 按天遍历
    totalDays += 1
    parseDay = item['parseDay']  
    tables += '<h4>'+parseDay+'</h4>'
    tables +='<table>'
    tables += '<tr>'
    tables += '<td class="ar ah">选中日</td>'
    tables += '<td class="ar ah">代码</td>'
    tables += '<td class="ar ah">名称</td>'
    tables += '<td class="ar ah">买入价</td>'
    tables += '<td class="ar ah">卖出日</td>'
    tables += '<td class="ar ah">卖出价</td>'
    tables += '<td class="ar ah">持股天数</td>'
    tables += '<td class="ar ah">区间最低价</td>'
    tables += '<td class="ar ah">区间最高价</td>'
    tables += '<td class="ar ah">区间最低收益</td>'
    tables += '<td class="ar ah">区间最高收益</td>'
    tables += '<td class="ar ah">收益率</td>'
    tables += '</tr>'
    
    dayTotalTradeNum = 0  # 日交易总数
    dayTotalGrowthRate = 0 # 日总收益率（总盈利 + 总亏损）
  
    dayTotalWinNum = 0 # 日总赢利数
    dayTotalWinRate = 0  # 日总赢利

    dayTotalLoseNum = 0 # 日总亏损数
    dayTotalLoseRate = 0  # 日总亏损
    
    print parseDay
    for i in item['idList']: # 遍历一天中的所有交易
      totalTradeNum += 1
      code = i['id']
      name = i['name']
      inPrice = float(i['inPrice'])
      outPrice = float(i['outPrice'])
      print parseDay,i['id']
      gr = (outPrice - inPrice)/inPrice

      totalGrowthRate += gr
      if gr > 0:
        totalWinNum += 1
        totalWinRate += gr
      else:
        totalLoseNum += 1
        totalLoseRate += gr
      
      dayTotalTradeNum += 1
      dayTotalGrowthRate += gr
      if gr > 0:
        dayTotalWinNum += 1
        dayTotalWinRate += gr
      else:
        dayTotalLoseNum += 1
        dayTotalLoseRate += gr

      minGr = (float(i['minPrice']) - inPrice)/inPrice
      maxGr = (float(i['maxPrice']) - inPrice)/inPrice

      tables += '<tr>'
      tables += '<td class="al">'+str(parseDay)+'</td>'
      tables += '<td class="al">'+str(i['id'])+'</td>'
      tables += '<td class="al">'+str(i['name'])+'</td>'
      tables += '<td class="al">'+str(i['inPrice'])+'</td>'
      tables += '<td class="al">'+str(i['outDay'])+'</td>'
      tables += '<td class="al">'+str(i['outPrice'])+'</td>'
      tables += '<td class="al">'+str(i['holdDays'])+'</td>'
      
      tables += '<td class="al">'+str(i['minPrice'])+'</td>'
      tables += '<td class="al">'+str(i['maxPrice'])+'</td>'

      if minGr > 0:
        tables += '<td class="al"><font color="red"><b>'+str(round(minGr*100.0,3))+'%</b></font></td>'
      elif minGr <= -0:
        tables += '<td class="al"><font color="green"><b>'+str(round(minGr*100.0,3))+'%</b></font></td>'

      if maxGr > 0:
        tables += '<td class="al"><font color="red"><b>'+str(round(maxGr*100.0,3))+'%</b></font></td>'
      elif maxGr <= -0:
        tables += '<td class="al"><font color="green"><b>'+str(round(maxGr*100.0,3))+'%</b></font></td>'

      if gr > 0:
        tables += '<td class="al"><font color="red"><b>'+str(round(gr*100.0,3))+'%</b></font></td>'
      elif gr <= -0:
        tables += '<td class="al"><font color="green"><b>'+str(round(gr*100.0,3))+'%</b></font></td>'


      tables += '</tr>'
    tables += '</table>'
    if 0!= dayTotalTradeNum:
      totalDayAvgGrowthRate += dayTotalGrowthRate/dayTotalTradeNum

  #if dayTotalTradeNum!=0: # 若当日无交易，则不参与统计
  #  totalDayAvgGrowthRate += dayTotalGrowthRate/dayTotalTradeNum
  winTradeAvgGr = 0
  loseTradeAvgGr = 0
  if 0!=totalWinNum:
    winTradeAvgGr = totalWinRate/totalWinNum
  if 0!=totalLoseNum:
    loseTradeAvgGr = totalLoseRate/totalLoseNum
  # ================================================================================
  s += '<table>'
  s += '<tr>'
  s += '<td class="ar ah">开始日期</td>'
  s += '<td class="ar ah">结束日期</td>'
  s += '<td class="ar ah">交易天数</td>'
  s += '<td class="ar ah">交易总数</td>'
  s += '<td class="ar ah">日均交易数</td>'

  s += '<td class="ar ah">涨</td>'
  s += '<td class="ar ah">跌</td>'
  s += '<td class="ar ah">胜率</td>'

  s += '<td class="ar ah">赢利交易平均收益率</td>'
  s += '<td class="ar ah">亏损交易平均收益率</td>'
  s += '<td class="ar ah"><b>日均收益率</b></td>'
  s += '<td class="ar ah">单笔交易平均收益率</td>'
  s += '</tr>'



  s += '<tr>'
  s += '<td class="ar">'+beginDate+'</td>'
  s += '<td class="ar">'+endDate+'</td>'
  s += '<td class="ar">'+str(totalDays)+'</td>'
  s += '<td class="ar">'+str(totalTradeNum)+'</td>'
  s += '<td class="ar">'+str(totalTradeNum/totalDays)+'</td>'

  s += '<td class="ar">'+str(totalWinNum)+'</td>'
  s += '<td class="ar">'+str(totalLoseNum)+'</td>'
  s += '<td class="ar">'+str(round(totalWinNum*100.0/totalTradeNum,3))+'%</td>'

  s += '<td class="ar">'+str(round(winTradeAvgGr*100.0,3))+'%</td>'
  s += '<td class="ar">'+str(round(loseTradeAvgGr*100.0,3))+'%</td>'
  s += '<td class="ar">'+str(round(totalDayAvgGrowthRate*100.0/totalDays,3))+'%</td>'
  s += '<td class="ar">'+str(round(totalGrowthRate*100.0/totalTradeNum,3))+'%</td>'
  s += '</tr>'
  s += '</table>'
  # ================================================================================
  

  s += tables

  s += '</body></html>'
  path = Tools.getReportDirPath()+'/trace-report.html'
  open(path,'w').write(s)
  os.system('open '+path)




