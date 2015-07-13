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
br.open('http://dir.indiamart.com')
tx = br.response().read()
soup = BeautifulSoup(tx)
categories = soup.findAll('div', class_='catHd')
data = []
for i in range(len(categories)):
  try:
    categoryname = categories[i].find('a').string
  except:
    categoryname = 'Not-available'
  br.open(categories[i].find('a')['href'])
  tx = br.response().read()
  soup = BeautifulSoup(tx)
  uls = soup.find('div', class_='mid').findAll('ul')
  a = []
  for m in range(len(uls)):
    lis = uls[m].findAll('li')
    for n in range(len(lis)):
      a.append(lis[n])
  for j in range(len(a)):
    try:
      subcatergory = a[j].find('a').string;
    except:
      subcatergory = 'Not-available'
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
        try:
          url = y[l]['href']
        except:
          url = 'Not-available'
        try:
          category = y[l].decode_contents(formatter="html").split("</span>")[1]
        except:
          category = 'Not-available'
        print(categoryname+','+subcatergory+','+category+','+url)