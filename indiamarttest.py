import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import csv
import re

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open('http://www.sourbook.com/zipavuj.php?G7eeqpILGqJt8oq2cI0jxA=Q6tQjN5FbYJdlaouGd0SIZtmoQlUgU86MUeNLi71P8yn9daZZT3BIr3mUQNAd9Bxc0zuRoZOA3Qmy%2Fqil76lRg%3D%3D')
tx = br.response().read()
soup = BeautifulSoup(tx)
a = soup.findAll('li', class_='q_cb')
for j in range(2,20):
  subcatergory = a[j].find('a').string;
  br.open(a[j].find('a')['href'])
  tx = br.response().read()
  soup = BeautifulSoup(tx)
  try:
    x = soup.findAll('p', class_='cat-lst')
  except:
    x = ""
  for k in range(len(x)):
    y = x[k].findAll('a')
    for l in range(len(y)):
      # print (y[j].decode_contents(formatter="html").split("</span>")[1],y[j]['href'])
      br.open(y[l]['href'])
      tx = br.response().read()
      soup = BeautifulSoup(tx)
      category = y[l].decode_contents(formatter="html").split("</span>")[1]
      suppliers =  soup.find('p', class_='flt_wd').decode_contents(formatter="html").split(" ")[0]
      print('Industrial Plant & Machine'+','+subcatergory+','+category+','+suppliers)