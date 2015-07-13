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
  # print(categories[i].find('a').string ,categories[i].find('a')['href'] )
  br.open(categories[i].find('a')['href'])
  tx = br.response().read()
  soup = BeautifulSoup(tx)
  a = soup.findAll('li', class_='q_cb')
  for j in range(len(a)):
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
        data.append(categories[i].find('a').string+','+subcatergory+','+category+','+suppliers+'\n')
with open("output.csv", "wb") as f:
  f.writelines(data)