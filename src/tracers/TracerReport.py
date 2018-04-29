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
  total = 0
  totalPr = 0
  totalGrowthRate = 0
  totalRiskRate = 0
  totalHoldDays = 0
  tables = ''
  for item in data:
    parseDay = item['parseDay']  
    tables += '<h4>'+parseDay+'</h4>'
    tables +='<table>'
    tables += '<tr>'
    tables += '<td>代码</td>'
    tables += '<td>PR</td>'
    tables += '<td>涨幅</td>'
    tables += '<td>买入价</td>'
    tables += '<td>初始止损价</td>'
    tables += '<td>初始止损幅度</td>'
    tables += '<td>卖出价</td>'
    tables += '<td>持股天数</td>'
    tables += '</tr>'
    for i in item['idList']:
      total += 1
      totalPr += i['PR']
      totalGrowthRate += i['growthRate']
      totalRiskRate += i['riskRate']
      totalHoldDays += i['holdDays']

      tables += '<tr>'
      tables += '<td>'+str(i['id'])+'</td>'
      tables += '<td>'+str(i['PR'])+'</td>'

      growthRate = i['growthRate']
      if growthRate >= 0.1:
        tables += '<td><font color="red"><b>'+str(i['profitRate'])+'</b></font></td>'
      elif growthRate <= -0.05:
      	tables += '<td><font color="green"><b>'+str(i['profitRate'])+'</b></font></td>'
      else:
      	tables += '<td>'+str(i['profitRate'])+'</td>'

      tables += '<td>'+str(i['inPrice'])+'</td>'
      tables += '<td>'+str(i['islp'])+'</td>'
      tables += '<td>'+str(i['riskRate']*100.0)+'%</td>'
      tables += '<td>'+str(i['outPrice'])+'</td>'
      tables += '<td>'+str(i['holdDays'])+'</td>'
    
      tables += '</tr>'
    tables += '</table>'

  avgPr = totalPr/total
  avgGrowthRate = totalGrowthRate/total
  avgRiskRate = totalRiskRate/total
  avgHoldDays = totalHoldDays/total

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
}

table {
	width: 100%;
	padding: 0;
	border: 1px;
	border-radius: 0.8em;
	cellspacing="0";
	margin-bottom: 50px;
	border-collapse: collapse;
	border-right: 1px solid #C1DAD7;
	border-bottom: 1px solid #C1DAD7;
	background: #fff;
	color: #4f6b72;
	text-align: center;
}


td {
	padding: 6px 6px 6px 12px;
	text-align: center;
}
</style>
  '''
  s += '</head><body>'
  s += '<table>'
  s += '<tr><td>总数：</td><td>'+str(total)+'</td></tr>'
  s += '<tr><td>PR平均值：</td><td>'+str(avgPr)+'</td></tr>'
  s += '<tr><td>平均涨幅：</td><td>'+str(round(avgGrowthRate*100.0,5))+'%</td></tr>'
  s += '<tr><td>平均风险幅度：</td><td>'+str(avgRiskRate)+'</td></tr>'
  s += '<tr><td>平均持股天数：</td><td>'+str(avgHoldDays)+'</td></tr>'
  s += '</table>'
  # ================================================================================
  

  s += tables

  s += '</body></html>'
  path = Tools.getReportDirPath()+'/trace-report.html'
  open(path,'w').write(s)
  os.system('open '+path)




