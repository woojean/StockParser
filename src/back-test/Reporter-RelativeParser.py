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



def fillGr(d,v):
  if v < -0.2:
    d['A[,-20%)'] += 1
  elif -0.2 <= v < -0.18:
    d['B[-20%,-18%)'] += 1
  elif -0.18 <= v < -0.16:
    d['C[-18%,-16%)'] += 1
  elif -0.16 <= v < -0.14:
    d['D[-16%,-14%)'] += 1
  elif -0.14 <= v < -0.12:
    d['E[-14%,-12%)'] += 1
  elif -0.12 <= v < -0.10:
    d['F[-12%,-10%)'] += 1
  elif -0.1 <= v < -0.08:
    d['G[-10%,-8%)'] += 1
  elif -0.08 <= v < -0.06:
    d['H[-8%,-6%)'] += 1
  elif -0.06 <= v < -0.04:
    d['I[-6%,-4%)'] += 1
  elif -0.04 <= v < -0.02:
    d['J[-4%,-2%)'] += 1
  elif -0.02 <= v < 0:
    d['K[-2%,0%)'] += 1
  elif 0 <= v < 0.02:
    d['L[0%,2%)'] += 1
  elif 0.02 <= v < 0.04:
    d['M[2%,4%)'] += 1
  elif 0.04 <= v < 0.06:
    d['N[4%,6%)'] += 1
  elif 0.06 <= v < 0.08:
    d['O[6%,8%)'] += 1
  elif 0.08 <= v < 0.1:
    d['P[8%,10%)'] += 1
  elif 0.1 <= v < 0.12:
    d['Q[10%,12%)'] += 1
  elif 0.12 <= v < 0.14:
    d['R[12%,14%)'] += 1
  elif 0.14 <= v < 0.16:
    d['S[14%,16%)'] += 1
  elif 0.16 <= v < 0.18:
    d['T[16%,18%)'] += 1
  elif 0.18 <= v < 0.2:
    d['U[18%,20%)'] += 1
  elif 0.2 <= v:
    d['V[20%,)'] += 1

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
  totalTradeDays = 0

  totalTradeNum = 0  # 交易总数
  totalGrowthRate = 0 # 总收益率（总盈利 + 总亏损）
  
  totalWinNum = 0 # 总赢利数
  totalWinRate = 0  # 总赢利

  totalLoseNum = 0 # 总亏损数
  totalLoseRate = 0  # 总亏损
  
  totalDayAvgGrowthRate = 0

  minMap = {
    'A[,-20%)':0,
    'B[-20%,-18%)':0,
    'C[-18%,-16%)':0,
    'D[-16%,-14%)':0,
    'E[-14%,-12%)':0,
    'F[-12%,-10%)':0,
    'G[-10%,-8%)':0,
    'H[-8%,-6%)':0,
    'I[-6%,-4%)':0,
    'J[-4%,-2%)':0,
    'K[-2%,0%)':0,
    'L[0%,2%)':0,
    'M[2%,4%)':0,
    'N[4%,6%)':0,
    'O[6%,8%)':0,
    'P[8%,10%)':0,
    'Q[10%,12%)':0,
    'R[12%,14%)':0,
    'S[14%,16%)':0,
    'T[16%,18%)':0,
    'U[18%,20%)':0,
    'V[20%,)':0
  }
  maxMap = {
    'A[,-20%)':0,
    'B[-20%,-18%)':0,
    'C[-18%,-16%)':0,
    'D[-16%,-14%)':0,
    'E[-14%,-12%)':0,
    'F[-12%,-10%)':0,
    'G[-10%,-8%)':0,
    'H[-8%,-6%)':0,
    'I[-6%,-4%)':0,
    'J[-4%,-2%)':0,
    'K[-2%,0%)':0,
    'L[0%,2%)':0,
    'M[2%,4%)':0,
    'N[4%,6%)':0,
    'O[6%,8%)':0,
    'P[8%,10%)':0,
    'Q[10%,12%)':0,
    'R[12%,14%)':0,
    'S[14%,16%)':0,
    'T[16%,18%)':0,
    'U[18%,20%)':0,
    'V[20%,)':0
  }

  value = 1.0
  
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
    

    # print parseDay
    for i in item['idList']: # 遍历一天中的所有交易
      totalTradeNum += 1
      code = i['id']
      name = i['name']
      inPrice = float(i['inPrice'])
      outPrice = float(i['outPrice'])
      # print parseDay,i['id']
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

      fillGr(minMap,minGr)
      fillGr(maxMap,maxGr)

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
      dayAvgGrowthRate = dayTotalGrowthRate/dayTotalTradeNum
      print (dayAvgGrowthRate)
      # value += value * dayAvgGrowthRate
      value = value * (1 + dayAvgGrowthRate)
      totalDayAvgGrowthRate += dayAvgGrowthRate
      totalTradeDays += 1

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
  s += '<td class="ar ah">按日累计收益值</td>'
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
  s += '<td class="ar">'+str(round(totalDayAvgGrowthRate*100.0/totalTradeDays,3))+'%</td>'
  s += '<td class="ar">'+str(round(totalGrowthRate*100.0/totalTradeNum,3))+'%</td>'
  s += '<td class="ar">'+str(value)+'</td>'
  s += '</tr>'
  s += '</table>'



  # ================================================================================
  intervalMap = sorted(minMap.keys())
  countTable = '<table>'
  for k in intervalMap:
    countTable += '<tr>'
    countTable += '<td>' + str(k) + '</td><td>' + str(minMap[k]) + '</td>'
    countTable += '</tr>'
  countTable += '</table>'
  
  countTable += '<table>'
  for k in intervalMap:
    countTable += '<tr>'
    countTable += '<td>' + str(k) + '</td><td>' + str(maxMap[k]) + '</td>'
    countTable += '</tr>'
  countTable += '</table>'
  
  s += countTable

  s += tables # 

  s += '</body></html>'
  path = Tools.getReportDirPath()+'/trace-report.html'
  open(path,'w').write(s)
  os.system('open '+path)




