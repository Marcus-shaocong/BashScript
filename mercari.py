# -*- coding: utf-8 -*-
import urllib
import urllib2
import traceback
from bs4 import BeautifulSoup
import pdb
import sys
import mechanize
import contextlib
##from selenium import webdriver
##from selenium.webdriver.common.by import By
##from selenium.webdriver.common.keys import Keys
##from selenium.webdriver.support.ui import WebDriverWait
##from selenium.webdriver.support.ui import Select
##from selenium.common.exceptions import NoSuchElementException
##from selenium.common.exceptions import NoAlertPresentException
##from selenium.webdriver.support import expected_conditions as EC
##from selenium.webdriver.common.action_chains import ActionChains
import json
import urlparse
import time
import pprint
import threading 
from threading import Thread
from Queue import Queue
from time import sleep, time
from datetime import timedelta, date
import re



##driver = webdriver.Chrome()
##
##driver.get(url)
##content = driver.page_source
##soup = BeautifulSoup(content)



##url = "https://www.rong360.com/gl/xinshoudaikuangonglue/list_20_1.html"
##content = urllib2.urlopen(url)
##content = content.read()
##soup = BeautifulSoup(content,'html.parser')
##ques = soup.findAll('li')
##for litag in ques:
##  linkTag = litag.find('a').get_text()
##  orgLink = urlparse.urljoin(url,linkTag.get('href'))
##
##
##
##globalUrl = set()

class Worker(Thread):
  """Thread executing tasks from a given tasks queue"""
  def __init__(self, tasks):
    Thread.__init__(self)
    self.tasks = tasks
    self.daemon = True
    self.start()

  def run(self):
    while True:
      func, args, kargs = self.tasks.get()
      try: func(*args, **kargs)
      except Exception, e: print e
      self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
      self.tasks = Queue(num_threads)
      for _ in range(num_threads): Worker(self.tasks)
                                                                                                                                                  
    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))
    
    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


def store_data(wline):
  global lock, output
  lock.acquire()
  output.write(wline)
  lock.release()

def fetch_detail(url, b):
    try:
      line = ""
##      b = mechanize.Browser()
##      b.set_handle_robots(False)
##      b.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
      content = b.open(url)
      con = content.read()
      soup = BeautifulSoup(con)
      itemName = soup.find('h2',class_="item-name").text
      itemName = itemName.replace(",", " ")
      #print itemName
      itemWording = soup.find('p',class_='item-wording').text
      itemWording = itemWording.replace(",", " ")
      #print itemWording
      itemTable = soup.find('table',class_="item-detail-table")

      trs = itemTable.find_all("tr")
      tableRows = 0
      detailLine = ""
      for tr in trs:
          th = tr.find("th").text
          #print "th:" + th
          td = tr.find("td").text
          if tableRows == 0:
              td = td.split("\n")[1].strip()

          elif tableRows == 1:
              #print type(td.split("\n"))
              td = "|" . join([ x.strip() for x in td.strip().split('\n\n')])
          elif tableRows == 3:
              if th == u"商品のサイズ":
                td = td.strip()
              else:
                 td = ","
          else:
            td = td.strip()
              
          #print "td:" + td
          tableRows += 1
          #print "============"
          if td == "":
              td = "N/A"
          detailLine = detailLine + td +","
          
      #print detailLine
      return detailLine
          
    except:
        print(traceback.format_exc())
        print "url:" + url
        return ","

        
def fetch_data(url):
    try:
      line = ""
      b = mechanize.Browser()
      b.set_handle_robots(False)
      b.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
      content = b.open(url)
      con = content.read()
      soup = BeautifulSoup(con)
      items = soup.find_all('section',class_='items-box')
      for item in items:
          line = ""
          itemLink = item.find("a")['href']
          #print itemLink
          details = fetch_detail(itemLink, b)
     
          title = item.find("h3", class_="items-box-name").text
          title.replace(",", "")
          #print "title: " + title
          price = item.find("div", class_="items-box-price").text
          price = price.replace(",","")
          #print "price:" + str(price)
          img = item.find("img")["data-src"]
          #print "img:"+ img
          line = title+","+price+"," + details +itemLink+","+img 
          print line
          store_data(line.encode('UTF-8','ignore')+'\n')
    except:
        print(traceback.format_exc())
        print "url:" + url

        
if __name__ == '__main__':
    start_time = time()
    global lock, output
    lock = threading.Lock()
    output = open("mercari.csv","w")
    pool = ThreadPool(30)
    for cao in range(1, 997):
      for page in range(1,101):
          url = "https://www.mercari.com/jp/category/"+str(cao)+"/?page="+str(page)
          pool.add_task(fetch_data,url)

    pool.wait_completion()
    output.close()
    end_time = time()
    time_taken = end_time - start_time
    print str(time_taken) + " seconds" 


