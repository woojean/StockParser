#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-03
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


class HotPointSniffer: 
  _source = 'hotpoint'
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
    if HotPointSniffer.isNew():
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
    f = open(path+'bkdict','w')
    f.write(str(d))
    f.close()

  def dumpTopBkDict(self,bkList):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    f = open(path+'topbkdict','w')
    f.write(str(bkList))
    f.close()

  def getTopBkListFromFile(self):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    path = path + 'topbkdict'
    d = eval(open(path,'r').read())
    return d

  def getBkInfoFromFile(self,bk):
    path = self.getRootPath()+'/data/'+self._dataPath+'/'
    path = path + 'bkdict'
    d = eval(open(path,'r').read())
    return d[bk]
  


  def getTopBkList(self,n):
    print 'getTopBkList...'
    d = self.getRootPath()+'/data/'+self._dataPath+'/'
    bkList = []
    topBkList = []
    for bk,url in self._BKs.items():
      path = d + bk
      res = open(path,'r').read()
      l = re.findall('"(.*?)"', res)
      for item in l:
        arr = item.split(',')
        '''
        ['1', 'BK0458', '\xe4\xbb\xaa\xe5\x99\xa8\xe4\xbb\xaa\xe8\xa1\xa8', '1.95', '268981406042', '1.27', '38|2|3|2', '300007', '2', '\xe6\xb1\x89\xe5\xa8\x81\xe7\xa7\x91\xe6\x8a\x80', '15.97', '9.99', '300515', '2', '\xe4\xb8\x89\xe5\xbe\xb7\xe7\xa7\x91\xe6\x8a\x80', '11.00', '-2.65', '2', '7671.56', '146.92']
        '''
        if 'BK' != arr[1][:2]:
          continue
        #if arr[1] in ['BK0816','BK0815']:  # BK0816 昨日连板，BK0815 昨日涨停
        #  continue
        bkData = (arr[1],arr[2],arr[3])  # 板块编码、板块名称、板块涨幅
        bkList.append(bkData)
    length = len(bkList)
    print "\n板块总数："+str(length)+"\n"
    self.dumpBkDict(bkList)  # 保存文件到本地方便后续查询
    bkList = sorted(bkList,key=lambda x: (-float(x[2])if('-'!=x[2])else(0)))
    #bkList = sorted(bkList,key=itemgetter(2), reverse=True)
    #topBkList = bkList[:n]
    topBkList = bkList[:n]
    self.dumpTopBkDict(topBkList)
    return topBkList

  
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

  def getIdList(self,n):
    print 'getIdList...'
    count = {}
    d = self.getRootPath()+'/data/'+self._dataPath+'/'
    for root,dirs,files in os.walk(d):
      for f in files:
        try:
          if 'BK'== f[:2]:
            path = root + f
            res = open(path,'r').read()
            l = re.findall('"(.*?)"', res)
            for item in l:
              '''
              2018-05-03 
              2,002681,奋达科技,9.41,0.86,10.06%,9.71,165823,153715449,8.55,8.59,9.41,8.58,-,-,-,-,-,-,-,-,0.00%,2.99,2.28,64.40,2012-06-05
              
              1 代码  2 名称  3 价格  4 价格增长  5 涨幅  6 振幅  23 换手率
              '''
              arr = item.split(',')
              id = arr[1]
              if 6 == len(id):
                if count.has_key(id):
                  count[id]['bkList'].append(f)
                else:
                  count[id] = {}
                  count[id]['basicInfo'] = arr
                  count[id]['bkList'] = [f]
        except Exception, e:
          pass
          print repr(e)
    filterdIdList = []
    for id,data in count.items():
      if len(data['bkList']) >= n:
        filterdIdList.append((id,data))
    return filterdIdList


  def dumpReport(self,idList,matchNum):
    print 'dumpReport...'
    sel = ''
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
  border-bottom: thin dotted #ccc;
  border-left: thin dotted #ccc;
  border-right: thin dotted #ccc;
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
  border-left: thin dotted #ccc;
  border-right: thin dotted #ccc;
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
  background-color:#F0FFFF;
}
</style>
  '''
    s += '</head><body>'

    bkList = self.getTopBkListFromFile()
    length = len(bkList)
    index = 1
    #i = 0
    s += '<table width="100%" cellspacing="0" cellpadding="0">'
    tr1 = '<tr>'
    tr2 = '<tr>'
    tr3 = '<tr>'
    for data in bkList:
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
      #	s +="<br/>"
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
     
      if len(data['bkList']) > matchNum and islp < 4.0 and islp !=0:
        trs +='<tr class="match">'
        sel += data['basicInfo'][1]+','
      else:
        trs +='<tr>'
      
      trs +='<td>'+str(index)+'</td>'

      # 代码
      trs +='<td>'+data['basicInfo'][1]+'</td>'

      # 名称
      trs +='<td><b>'+data['basicInfo'][2]+'</b></td>'

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
        trs +='<td><font color="#009ACD"><b>'+str(islp)+'%</b></font></td>'
      else:
        trs +='<td>'+str(islp)+'%</td>'

      # 板块
      bks = ''
      for bk in data['bkList']:
        bkInfo = self.getBkInfoFromFile(bk)
        bks += '<label class="tag">'+bkInfo[1] +'</label>'
      if len(data['bkList']) > matchNum:
        trs +='<td><font color="#009ACD">'+bks+'</font></td>'
      else:
        trs +='<td>'+bks+'</td>'

      

      trs +='</tr>'
      parsedNum += 1
      index += 1
    s += trs
    s += '</table>'
    s += '</body></html>'
    parseTime = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())) 
    path = Tools.getReportDirPath()+'/HotPoint-'+parseTime+'.html'
    open(path,'w').write(s)

    selPath = Tools.getReportDirPath()+'/HotPoint-'+parseTime+'.sel'
    open(selPath,'w').write(sel)
    print path

    os.system('open '+path)
  
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
    # 获取板块数据
    self.genBKdata()

    # 获取前十板块
    bkList = self.getTopBkList(TOP_BK_NUM)  # <--------------------

    # 获取板块个股数据
    self.genBkStockData(bkList)
    # idList 
    idList = self.getIdList(RESONANCE_NUM)  # <--------------------
    print idList
    
    self.dumpReport(idList,RESONANCE_NUM)


# config
# ===============================================================
TOP_BK_NUM = 28  # Top 5% + 2
RESONANCE_NUM = 3 # Resonance atleast 2


if __name__ == '__main__':
  print 'HotPointSniffer'
  HotPointSniffer().initDir()
  sniffer = HotPointSniffer()
  sniffer.run()



