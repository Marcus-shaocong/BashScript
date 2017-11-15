# -*- coding: utf-8 -*-
import os
from fake_useragent import UserAgent
import re
import urllib
import urllib2
import traceback
from bs4 import BeautifulSoup
import pdb
import sys
import mechanize
import contextlib
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
import random


ua = UserAgent(cache=True)
##bro = mechanize.Browser()
##bro.set_handle_robots(False)
randomAgent = set()
ipProxies = []

remainURL = set()
alreadyURL = set()
urls = []


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
        
def get_user_agents():
    while True:
        randomAgent.add(ua.random)
        if len(randomAgent) == 10:
            break;

def fetch_detail(url):
    try:
      line = ""
      bro = mechanize.Browser()
      bro.set_handle_robots(False)
##      b.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
      agent = random.choice(list(randomAgent))
      print agent
      bro.addheaders=[('User-agent',agent)]
      proxy = random.choice(ipProxies)
      print proxy
      if proxy:
         bro.set_proxies({'http':proxy})   
      content = bro.open(url)
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

def get_proxies():
    global ipProxies
    output=os.system("proxybroker find --types HTTP HTTPS --limit 10 --outfile proxy.txt")
    print output
    proxy = open("proxy.txt", "r")
    for line in proxy.readlines():
        ipaddress = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d+",line)
        ipProxies += ipaddress
    #ipProxies = [ "http://" + x for x in ipProxies]
    proxy.close()

def generate_urls():
    global urls, remainURL, alreadyURL
    url = 'https://www.mercari.com/jp/category/%d/?page=%d'
    urls = [url % (pid, t) for pid in range(1,996) for t in range(1, 99)]
    remainURL = set(urls)


def get_random_urls():
    global urls, remainURL, alreadyURL, lock
    #lock.acquire()
    newURL=""
    newURL = random.choice(urls)
    #print ("new1:" + newURL)
    while newURL in alreadyURL and remainURL:
        newURL=random.choice(urls)

    #print ("new2:"+newURL)
    alreadyURL.add(newURL)
    if newURL in remainURL:
        remainURL.remove(newURL)
    #lock.release()
    return newURL

def fetch_data(url):
    try:
      line = ""
      bro = mechanize.Browser()
      bro.set_handle_robots(False)
##      b.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
      agent = random.choice(list(randomAgent))
      print agent
      bro.addheaders=[('User-agent',agent)]
      proxy = random.choice(ipProxies)
      print proxy
      if proxy:
         bro.set_proxies({'http':proxy})      
      content = bro.open(url)
      con = content.read()
      soup = BeautifulSoup(con)
      items = soup.find_all('section',class_='items-box')
      for item in items:
          line = ""
          itemLink = item.find("a")['href']
          #print itemLink
          details = fetch_detail(itemLink)
     
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
    get_user_agents()
    get_proxies()
    print random.choice(ipProxies)
    generate_urls()
    print("remainURL length", len(remainURL))
    #print(urls)
    #agent = random.choice(list(randomAgent))
    #print agent

    output = open("mercari.csv","w")
    pool = ThreadPool(30)
    while remainURL:
        url = get_random_urls()
        print ("final:"+url)
        pool.add_task(fetch_data,url)

    pool.wait_completion()
    output.close()
    end_time = time()
    time_taken = end_time - start_time
    print str(time_taken) + " seconds" 
