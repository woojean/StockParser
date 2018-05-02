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



if __name__ == '__main__':
  pass
  f = 'trace_report.data'
  p = Tools.getTracerDirPath()+'/'+f
  s = open(p,'r').read()
  data = eval(s)

  # ================================================================================
  beginSelectDay = data[0]['parseDay'] 
  endSelectDay = data[-1]['parseDay'] 
  total = 0
  totalRise = 0
  totalDecline = 0
  totalDraw = 0
  totalGrowthRate = 0
  totalRiskRate = 0
  totalHoldDays = 0
  tables = ''
  totalDay = 0 # 有候选项的天数
  totalDayAvgSelectNum = 0
  totalDayAvgGrowthRate = 0  # 日均涨幅之和
  totalDayAvgWinRate = 0
  totalDayAvgHoldDays = 0
  totalDayAvgRiskRate = 0
  for item in data:
    parseDay = item['parseDay']  
    tables += '<h4>'+parseDay+'</h4>'
    tables +='<table>'
    tables += '<tr>'
    tables += '<td>买入日</td>'
    tables += '<td>代码</td>'
    tables += '<td>名称</td>'
    tables += '<td>涨幅</td>'
    tables += '<td>买入价</td>'
    tables += '<td>初始止损价</td>'
    tables += '<td>初始止损幅度</td>'
    tables += '<td>卖出价</td>'
    tables += '<td>持股天数</td>'
    tables += '</tr>'
    
    dayTotalGrowthRate = 0 # 当日总涨幅
    dayTotalWinRate = 0
    dayWinNum = 0
    dayTotal = len(item['idList'])  # 当日选股总数
    dayTotalHoldDays = 0
    dayTotalRiskRate = 0
    for i in item['idList']:
      total += 1
      totalGrowthRate += i['growthRate']
      totalRiskRate += i['riskRate']
      dayTotalRiskRate += i['riskRate']
      totalHoldDays += i['holdDays']
      dayTotalHoldDays += i['holdDays']

      if i['riskRate'] == i['growthRate']:
      	tables += '<tr style="background-color:#eee;">'
      else:
        tables += '<tr>'
      tables += '<td>'+str(i['day'])+'</td>'
      tables += '<td>'+str(i['id'])+'</td>'
      tables += '<td>'+str(i['name'])+'</td>'


      # 涨跌幅
      growthRate = i['growthRate']
      dayTotalGrowthRate += growthRate
      if growthRate > 0:
        dayWinNum +=1
      	totalRise += 1
      elif growthRate < 0:
      	totalDecline +=1
      else:
      	totalDraw +=1

      if growthRate >= 0.05:
        tables += '<td><font color="red"><b>'+str(i['profitRate'])+'</b></font></td>'
      elif growthRate <= -0.03:
      	tables += '<td><font color="green"><b>'+str(i['profitRate'])+'</b></font></td>'
      else:
      	tables += '<td>'+str(i['profitRate'])+'</td>'

      tables += '<td>'+str(i['inPrice'])+'</td>'
      tables += '<td>'+str(i['islp'])+'</td>'
      tables += '<td>'+str(i['riskRate']*100.0)+'%</td>'
      tables += '<td>'+str(i['outPrice'])+'</td>'
      tables += '<td>'+str(i['holdDays'])+'</td>'
    
      tables += '</tr>'
    
    # 算日均涨幅
    if len(item['idList']) > 0: # 当日有选股
      totalDay +=1  # 有选股的天数总计
      totalDayAvgGrowthRate += dayTotalGrowthRate/dayTotal  # 当日日均涨幅
      totalDayAvgWinRate += round(dayWinNum*1.0/len(item['idList']),5)
      totalDayAvgHoldDays += dayTotalHoldDays/dayTotal
      totalDayAvgRiskRate += dayTotalRiskRate/dayTotal
      totalDayAvgSelectNum += len(item['idList'])*1.0 #当日选股数
    tables += '</table>'
  
  avgRiskRate = round(totalRiskRate/total,5)
  avgHoldDays = totalHoldDays/total
  avgSelectNum = round(totalDayAvgSelectNum*1.0/totalDay,5)
  avgGrowthRate = round(totalGrowthRate*1.0/totalDay,5)

  avgDayHoldDays = round(totalDayAvgHoldDays*1.0/totalDay,5)
  avgDayRiskRate = round(totalDayAvgRiskRate/totalDay,5)
  avgDayWinRate = round(totalDayAvgWinRate/totalDay,5)
  avgDayGrowthRate = round(totalDayAvgGrowthRate/totalDay,5)

  # ================================================================================

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
	border: 1px solid #C1DAD7;
	background: #fff;
	color: #4f6b72;
	text-align: center;
}

.al{
  text-align: left;
}

.ar{
  width:50%;
  text-align: right;
}

</style>
  '''
  s += '</head><body>'
  s += '<table>'
  s += '<tr><td colspan=2><b>模拟交易报告</b></td></tr>'
  s += '<tr><td class="ar">交易区间：</td><td class="al">'+beginSelectDay+' ~ '+endSelectDay+'</td></tr>'
  s += '<tr><td class="ar">选股总数：</td><td class="al">'+str(total)+'</td></tr>'
  s += '<tr><td class="ar">涨：</td><td class="al">'+str(totalRise)+'</td></tr>'
  s += '<tr><td class="ar">跌：</td><td class="al">'+str(totalDecline)+'</td></tr>'
  s += '<tr><td class="ar">平：</td><td class="al">'+str(totalDraw)+'</td></tr>'
  s += '<tr><td class="ar">胜率：</td><td class="al">'+str(round(totalRise*100.0/total,3))+'%</td></tr>'
  s += '<tr><td class="ar">平均持股天数：</td><td class="al">'+str(avgHoldDays)+'</td></tr>'
  s += '<tr><td class="ar">平均初始止损幅度：</td><td class="al">'+str(avgRiskRate*100.0)+'%</td></tr>'
  s += '<tr><td class="ar">平均涨幅：</td><td class="al">'+str(avgGrowthRate*100.0)+'%</td></tr>'
  s += '</table>'

  s += '<table>'
  s += '<tr><td colspan=2><font><b>模拟交易分日统计</b></font><font>（只统计选股结果不为空的交易日）</font></td></tr>'
  s += '<tr><td class="ar"><font color="red">日平均选股数：</font></td><td class="al"><font color="red">'+str(avgSelectNum)+'</font></td></tr>'
  s += '<tr><td class="ar"><font color="red">日选股平均持股天数：</font></td><td class="al"><font color="red">'+str(avgDayHoldDays)+'</font></td></tr>'
  s += '<tr><td class="ar"><font color="red">日选股平均初始止损幅度：</font></td><td class="al"><font color="red">'+str(avgDayRiskRate*100.0)+'%</font></td></tr>'
  s += '<tr><td class="ar"><font color="red">日平均选股胜率：</font></td><td class="al"><font color="red">'+str(avgDayWinRate*100.0)+'%</font></td></tr>'
  s += '<tr><td class="ar"><font color="red"><b>日选股平均涨幅：</b></font></td><td class="al"><font color="red"><b>'+str(avgDayGrowthRate*100.0)+'%</b></font></td></tr>'
  s += '</table>'
  # ================================================================================
  

  s += tables

  s += '</body></html>'
  path = Tools.getReportDirPath()+'/trace-report.html'
  open(path,'w').write(s)
  os.system('open '+path)




