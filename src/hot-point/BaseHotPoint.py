#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-04
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new
from operator import itemgetter 

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
61 个行业  => 6
189 个概念 => 19
31 个地域  => 3
共281个板块
'''


class BaseHotPoint: 
  _source = ''
  _BKs = {
    'DY':'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKDY&sty=FPGBKI&sortType=(ChangePercent)&page=1&pageSize=200&js=var%20nJmHNLLU=\{rank:\[(x)\],pages:(pc),total:(tot)\}&token=7bc05d0d4c3c22ef9fca8c2a912d779c',
    'GN':'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=FPGBKI&sortType=(ChangePercent)&page=1&pageSize=200&js=var%20nJmHNLLU=\{rank:\[(x)\],pages:(pc),total:(tot)\}&token=7bc05d0d4c3c22ef9fca8c2a912d779c',
    'HY':'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=FPGBKI&sortType=(ChangePercent)&page=1&pageSize=200&js=var%20ItdXMnRk=\{rank:\[(x)\],pages:(pc),total:(tot)\}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'
  }
  
  def __init__(self): 
    self._dataPath = self._source
    self._failedDataPath = 'failed_' + self._source
  

  @staticmethod
  def isNew():
    isNew = False if (len(sys.argv) <= 1) else ('new' ==sys.argv[1])
    return isNew
  

  def getRootPath(self):
    return Tools.getRootPath()

  def initDir(self):
    if len(self._source) < 1:
      raise Exception("Exception：source未设置！")
    if BaseHotPoint.isNew():
      Tools.initDir(self._source)
      Tools.initDir('failed_' + self._source)
    else:
      Tools.touchDir(self._source)
      Tools.touchDir('failed_' + self._source)
  
  def dumpFile(self,id,data):
    path = (self.getRootPath()+'/data/'+self._failedDataPath+'/') if (len(data) < 100) else (self.getRootPath()+'/data/'+self._dataPath+'/')
    f = open(path+id,'w')
    f.write(data)
    f.close()

  def genBKdata(self):
    for bk,url in self._BKs.items():
      print bk
      data = requests.get(url,verify=False).text
      self.dumpFile(bk,data)

  def dumpBkDict(self,bkList):
    d = {}
    for bk in bkList:
      d[bk[0]] = bk
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    f = open(path+'bk-dict','w')
    f.write(str(d))
    f.close()

  def getBkInfoFromFile(self,bk):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    path = path + 'bk-dict'
    d = eval(open(path,'r').read())
    return d[bk]

  def dumpFilteredBkDict(self,bkList):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    f = open(path+'filtered-bk-dict','w')
    f.write(str(bkList))
    f.close()

  def getFilteredBkListFromFile(self):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    path = path +'filtered-bk-dict'
    d = eval(open(path,'r').read())
    return d
  

  
  def dumpReport(self,idList,matchNum):
    print 'dumpReport...'
    sel = ''
    csv = ''
    s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    s += '''
<style>
font-size:0.8em;

table {
}


td{
  font-size:0.8em;
  text-align:center;
  padding:5px;
  border-bottom: thin dotted #ccc;
}

tr:hover{
  background-color:yellow;
  cursor:pointer;
}

.header{
  border-right: thin solid #ccc;
  border-bottom: thin solid #ccc;
  font-weight:bold;
}

.tag{
  border-right: thin solid #ccc;
  border-bottom: thin solid #ccc;
  border-radius:3px;
  padding:3px;
  margin:5px;
  font-size:0.6em;
}

.bk{
  font-weight:bold;
  font-size:0.6em;
  border-right: thin solid #ccc;
  border-bottom: thin solid #ccc;
  padding:1px;
  text-align:center;
  margin-top:20px;
  margin-bottom:20px;
}

.bkindex{
  font-weight:lighter;
  font-size:0.6em;
}

.match{
  background-color:#FFFFE0;
}
</style>
  '''
    s += '</head><body>'

    bkList = self.getFilteredBkListFromFile()
    length = len(bkList)
    index = 1
    #i = 0
    s += '<table width="100%" cellspacing="0" cellpadding="0">'
    tr1 = '<tr>'
    tr2 = '<tr>'
    tr3 = '<tr>'
    for data in bkList:
      csv += data[1]+','
      tr1 += '<td width="'+str(100.0/length)+'%"><span class="bkindex" >'+str(index)+'</span></td>'
      tr2 += '<td class="bk">' + data[1] +'</td>'
      rate = float(data[2]) if ('-'!=data[2]) else(0)
      tr3 +='<td width="'+str(100.0/length)+'%" class="bk">'
      if rate > 0:
        tr3 +='<font color="red"> '+data[2]+'%</font>'
      else:
        tr3 +='<font color="green"> '+data[2]+'%</font>'
      tr3 += '</td>'
      index += 1
      #if (0 == i%5) and i>=3:
      # s +="<br/>"
      #i += 1
    tr1 += '</tr>'
    tr2 += '</tr>'
    tr3 += '</tr>'
    s += tr1
    s += tr2
    s += tr3
    s +='</table>'


    s += '<br/><br/>'


    s += '<table width="100%" cellspacing="0" cellpadding="0">'
    
    th = '<tr align="center" style="font-size:1.2em;">'
    th += '<td class="header">序号</td>'
    th += '<td class="header">代码</td>'
    th += '<td class="header">名称</td>'
    th += '<td class="header">涨幅</td>'
    th += '<td class="header">振幅</td>'
    th += '<td class="header">换手率</td>'
    th += '<td class="header"><font color="#009ACD">ISLP</font></td>'
    th += '<td class="header">所属板块</td>'
    th += '</tr>'
    s += th

    trs = ''
    parsedNum = 0
    index = 1
    total = len(idList)
    idList = sorted(idList,key=lambda i: (-len(i[1]['bkList'])))
    for item in idList:
      self.printProcess(parsedNum,total)
      data = item[1]
      
      # inittial stop lose price
      price = float(data['basicInfo'][3]) if ('-'!=data['basicInfo'][3]) else (0)
      minPrice = float(data['basicInfo'][12]) if ('-'!=data['basicInfo'][12]) else (0)
      islp = round((price-minPrice)/price,5)*100.0 if(0!=price*minPrice)else(0)
      
      match =False
      #if len(data['bkList']) > matchNum and islp < 4.0 and islp !=0:
      if islp < 4.0 and islp !=0:
        #trs +='<tr class="match">'
        trs +='<tr>'
        sel += data['basicInfo'][1]+','
        match = True
      else:
        trs +='<tr>'
      
      trs +='<td>'+str(index)+'</td>'

      # 代码
      trs +='<td>'+data['basicInfo'][1]+'</td>'

      # 名称
      #if match:
      #  trs +='<td>'+data['basicInfo'][2]+'</td>'
      #else:
      #  trs +='<td><font color="#009ACD"><b>'+data['basicInfo'][2]+'</b></font></td>'
      trs +='<td>'+data['basicInfo'][2]+'</td>'

      # 涨幅
      riseRate = float(data['basicInfo'][5].replace('%','')) if ('-'!=data['basicInfo'][5]) else (0)
      if 0 == riseRate:
        trs +='<td><b>'+data['basicInfo'][5]+'</b></td>'
      elif riseRate> 0:
        trs +='<td><font color="red"><b>'+data['basicInfo'][5]+'</b></font></td>'
      elif riseRate< 0:
        trs +='<td><font color="green"><b>'+data['basicInfo'][5]+'</b></font></td>'

      # 振幅
      if '-' == data['basicInfo'][6]:
        trs +='<td>'+data['basicInfo'][6]+'</td>'
      else:
        trs +='<td>'+data['basicInfo'][6]+'%</td>'
      

      # 换手率
      if '-' == data['basicInfo'][23]:
        trs +='<td>-</td>'
      else:
        trs +='<td>'+data['basicInfo'][23]+'%</td>'
      
      # ISLP
      if 0 == islp:
        trs +='<td>-</td>'
      elif islp<4.0:
        trs +='<td><font color="#009ACD" size=2><b>-'+str(islp)+'%</b></font></td>'
      else:
        trs +='<td><font color="#aaa">-'+str(islp)+'%</font></td>'

      # 板块
      bks = ''
      for bk in data['bkList']:
        bkInfo = self.getBkInfoFromFile(bk)
        bks += '<label class="tag">'+bkInfo[1] +'</label>'
      #if len(data['bkList']) > matchNum:
      #  trs +='<td><font color="#009ACD">'+bks+'</font></td>'
      #else:
      #  trs +='<td>'+bks+'</td>'
      trs +='<td>'+bks+'</td>'

      

      trs +='</tr>'
      parsedNum += 1
      index += 1
    s += trs
    s += '</table>'
    s += '</body></html>'
    parseTime = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
    path = Tools.getHotPointReportDirPath()+'/'+self._source+'-'+parseTime+'.html'
    open(path,'w').write(s)

    selPath = Tools.getHotPointReportDirPath()+'/'+self._source+'-'+parseTime+'.sel'
    open(selPath,'w').write(sel)

    csvPath = Tools.getHotPointReportDirPath()+'/'+self._source+'-'+parseTime+'.csv'
    open(csvPath,'w').write(csv)
    print path

    os.system('open '+path)


  def genBkStockData(self,bkList):
    print 'genBkStockData...'
    for bk in bkList:
      bkCode = bk[0]
      print bk[0],bk[1],bk[2]
      url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.'
      url += bkCode
      url += '1&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&'
      url += 'page=1&pageSize=1000&js=var%20ezMRpmTj=\{rank:\[(x)\],pages:(pc),total:(tot)\}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'
      data = requests.get(url,verify=False).text
      self.dumpFile(bkCode,data)

  def getFilteredBkList(self,n):
    pass

  def printProcess(self,current,total):
    lastRate = round((current-1)*100.0/total,0)
    currentRate = round(current*100.0/total,0)
    if lastRate != currentRate:
      rate = str(int(currentRate)) 
      rate = rate.rjust(3,' ')
      s = ''
      s = s.rjust(int(currentRate),'.')
      s += ' -> '
      s = s.ljust(104,' ')
      s += rate + ' %'
      print s

  def run(self):
    pass


# config
# ===============================================================

if __name__ == '__main__':
  print 'BaseHotPoint'



