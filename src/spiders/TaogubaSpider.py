#coding:utf-8
'''
woojean@2018-05-11
'''

import sys
import re
import requests
from BaseSpider import BaseSpider

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
reload(sys)
sys.setdefaultencoding('utf-8')

# ============================================================================================
class TaogubaSpider(BaseSpider):  
  _source = 'taoguba'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    url = 'https://www.taoguba.com.cn/index?pageNo='
    url += str(id)
    url += '&blockID=1&flag=0&pageNum=21303'
    return url


  '''
  <div class="p_list01 splist_div user_1004924" style="background:#f0f0f0">
              <ul>
                  <li class="pcdj07"><span title="积分：0" class="pclive_0"></span></li>
                  <li class="pcdj02"><span class="font_yy">原</span>
                  <a href="Article/1947449/1" title='苟且到明天'   target="_blank">苟且到明天</a><b>(143)</b></li>
                  <li class="pcdj08"><a id ="pop_1947449" href="blog/1004924" onmouseover="userTips(this,1004924);" onmouseout="offTip()" target="_blank">dadaming211 </a></li>
                  <li class="pcdj03">05-11 10:11</li>
                  <li class="pcdj04"><span>6</span>/1295</li>   <----------------------------------------------
                  <li class="pcdj05"><span>0</span>/0</li>
                  <li class="pcdj05">0</li>
                  <li class="pcdj06">2018-05-06</li>
              </ul>
             </div>
  '''
  def parseOnePage(self,res):
    articleList = []
    itemList = re.findall(r'p_list01([\s\S]*?)</div>', res)
    for item in itemList:
      response = int(re.findall(r'class="pcdj04"><span>([\s\S]*?)</span>', item)[0])
      if(response < MIN_RESPONSE):
        continue
      article = {}
      article['href'] = re.findall(r'href="([\s\S]*?)"', item)[0]
      article['title'] = re.findall(r'target="_blank">([\s\S]*?)</a>', item)[0]
      article['response'] = response
      articleList.append(article)
    return articleList


  def run(self):
    for id in self._idList:
      try:
        if self.isDataSuccess(id):
          continue
        url = self.genUrl(id)
        print str(self._threadId) + ' -> ' +str(id)
        res = requests.get(url,verify=False).text
        data = self.parseOnePage(res)
        self.dumpFile(id,str(data))
      except Exception, e:
        print repr(e)
        pass


MIN_RESPONSE = 100
MAX_PAGES = 21307
THREADS = 50


if __name__ == '__main__':

  threads = THREADS # 线程数（不能少于任务数）
  idList = []
  for pageNo in xrange(1,MAX_PAGES):
    idList.append(str(pageNo))

  TaogubaSpider().initDir()
  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = TaogubaSpider(subIdList,threadId)
    spider.start()

