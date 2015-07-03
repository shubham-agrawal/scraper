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
br.open('http://bigbasket.com/product/page/10')
br.open('http://bigbasket.com/pd/274120/sunpure-refined-sunflower-oil-1-ltr-pouch/')

# Common data
tx = br.response().read()
soup = BeautifulSoup(tx)

try:
  productName = soup.findAll('div', class_='uiv2-product-name')[0].findAll('h1')[0].string
except:
  productName = ""
try:
  companyName = soup.findAll('div', class_='uiv2-brand-name')[0].findAll('a')[0].string.replace("&amp;", "&")
except:
  companyName = ""
try:
  productPrice =  soup.findAll('div', class_='uiv2-price')[0].string
except:
  productPrice = ""
try:
  mrp = soup.findAll('div','uiv2-savings')[0].findAll('span')[0].decode_contents(formatter="html").split(":")[1]
except:
  mrp = ""
try:
  image = soup.findAll('div','uiv2-product-large-img-container')[0].find('a')['href'].split('//')[1]
except:
  image=""
try:
  sizeString = soup.findAll('div',class_='uiv2-product-size')[0].find(name="input",attrs={'type':'radio','checked':True}).parent.find('label').string.split('-')[0].strip()
  size = re.sub('\s+',' ',sizeString)
except:
  size = ""
try:
  collections = []
  breadcrumbhtml = soup.findAll('div','breadcrumb-item')
  for i in range(len(breadcrumbhtml)):
    collections.append(breadcrumbhtml[i].find('span').string.replace("&amp;", "&"))
except:
  collections = []

print(productName,companyName,productPrice,mrp,image,size,collections)
