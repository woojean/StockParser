#coding:utf-8
#!/usr/bin/env python
import math

'''
执行若干次某任务，某概率事件连续发生指定次数的概率研究

https://www.zhihu.com/question/59024257

单独执行一次某任务，事件A发生的概率为r
执行m次某任务，“事件A连续发生n次”（n<=m）出现的概率为：
Pm = Pm_1 + (1-Pm_n_1)*(1-r)*r^n
其中：
P0~Pn_1的概率为0；
Pn的概率为r^n
'''

def calculate(r,m,n):
  if (m <= (n-1)):
    return 0
  if m == n:
  	return math.pow(r, n)
  Pm_1 = calculate(r,m-1,n)
  Pm_n_1 = calculate(r,m-n-1,n)
  Pm = Pm_1 + (1-Pm_n_1)*(1-r)*math.pow(r, n)
  return Pm

if __name__ == '__main__':
  r = 0.4
  m = 200
  n = 10
  Pm = calculate(r,m,n)
  print Pm
  

















