'''
@Author: Javfa
@Date: 2020-03-26 12:45:03
@LastEditTime: 2020-03-31 10:23:31
@LastEditors: Javfa
@Description: In User Settings Edit
@FilePath: /projects/G7/expertsG7.py
'''
from selenium import webdriver
import mysql.connector
import requests
import re
import time

def urlMaker(name):
  return 'https://zjchacha.cn/search?q=' + name

def userInfoUrlMaker(uri):
  return 'https://api.zjchacha.cn/api/t?uri=' + uri + '&callback=resultcallbackUserInfo&token=qh4j35X0dXpWqHNvz6O_z4Cc0yO-rZKj06N_0IOu5EGC83U-0Y4C84Gw0mF-eh2v3Yt0710f8ZKC4FU3thCP3DCmtn7S8Ft77Ft3d4iEq6K-3EF-81iw4XK3r3UL440us58T3FvLemidsyFO'

def userTagUrlMaker(uri):
  return 'https://api.zjchacha.cn/api/tags?uri=' + uri + '&callback=resultcallbackUserTags&token=qh4j35X0dXpWqHNvz6O_z4Cc0yO-rZKj06N_0IOu5EGC83U-0Y4C84Gw0mF-eh2v3Yt0710f8ZKC4FU3thCP3DCmtn7S8Ft77Ft3d4iEq6K-3EF-81iw4XK3r3UL440us58T3FvLemidsyFO'

def coAutUrlMaker(uri):
  return 'https://api.zjchacha.cn/api/co-authors?uri=' + uri + '&level=1&callback=resultcallbackUserAuthors&token=qh4j35X0dXpWqHNvz6O_z4Cc0yO-rZKj06N_0IOu5EGC83U-0Y4C84Gw0mF-eh2v3Yt0710f8ZKC4FU3thCP3DCmtn7S8Ft77Ft3d4iEq6K-3EF-81iw4XK3r3UL440us58T3FvLemidsyFO'

def coComUrlMaker(uri):
  return 'https://api.zjchacha.cn/api/co-coms?uri=' + uri + '&callback=resultcallbackUserCompany&token=qh4j35X0dXpWqHNvz6O_z4Cc0yO-rZKj06N_0IOu5EGC83U-0Y4C84Gw0mF-eh2v3Yt0710f8ZKC4FU3thCP3DCmtn7S8Ft77Ft3d4iEq6K-3EF-81iw4XK3r3UL440us58T3FvLemidsyFO'

def sameDomUrlMaker(uri):
  return 'https://api.zjchacha.cn/api/same-domains?uri=' + uri + '&callback=resultcallbackSameDomain&token=qh4j35X0dXpWqHNvz6O_z4Cc0yO-rZKj06N_0IOu5EGC83U-0Y4C84Gw0mF-eh2v3Yt0710f8ZKC4FU3thCP3DCmtn7S8Ft77Ft3d4iEq6K-3EF-81iw4XK3r3UL440us58T3FvLemidsyFO'

def sameOrgUrlMaker(uri):
  return 'https://api.zjchacha.cn/api/same-orgs?uri=' + uri + '&callback=resultcallbackSameOrg&token=qh4j35X0dXpWqHNvz6O_z4Cc0yO-rZKj06N_0IOu5EGC83U-0Y4C84Gw0mF-eh2v3Yt0710f8ZKC4FU3thCP3DCmtn7S8Ft77Ft3d4iEq6K-3EF-81iw4XK3r3UL440us58T3FvLemidsyFO'

# 获得专家的uri
def getUri(i, u):
    time.sleep(10)
    browser.get(u)
    source = browser.page_source
    pattern = 'href="/detail\?uri=([^"]+)"><span class="person-detail-right-name">' + result[i][0] + '</span></a><span class="color-blue iconfont margin-left-10">\ue6d9</span><span class="person-detail-right-school">' + result[i][1]
    uri = re.findall(pattern, source)
    return uri

mydb = mysql.connector.connect(host='58.213.198.77', port = '10068', user='root', passwd='Ttxs0315!', database='techTransfer')
mycursor = mydb.cursor()

sql = 'select * from expertsG7 limit 2849,100'
mycursor.execute(sql)
result = mycursor.fetchall()
result = [list(i) for i in result]

urlList = [urlMaker(i[0]) for i in result]

browser = webdriver.Firefox()

browser.get('https://zjchacha.cn/search?q=%E8%A2%81%E9%9A%86%E5%B9%B3')
time.sleep(5)

uriList = [getUri(i, u) for i,u in enumerate(urlList)]

for i, name in enumerate(result):
    name.append(uriList[i])

userInfoUrlList = [(i[0], i[1], userInfoUrlMaker(i[2][0])) for i in result if len(i[2]) != 0]
userTagUrlList = [(i[0], i[1], userTagUrlMaker(i[2][0])) for i in result if len(i[2]) != 0]
coAutUrlList = [(i[0], i[1], coAutUrlMaker(i[2][0])) for i in result if len(i[2]) != 0]
coComUrlList = [(i[0], i[1], coComUrlMaker(i[2][0])) for i in result if len(i[2]) != 0]
sameDomUrlList = [(i[0], i[1], sameDomUrlMaker(i[2][0])) for i in result if len(i[2]) != 0]
sameOrgUrlList = [(i[0], i[1], sameOrgUrlMaker(i[2][0])) for i in result if len(i[2]) != 0]

# 从用uri拼接的url地址获取json
def getInfo(u):
    time.sleep(2)
    response = requests.get(u)
    return response.text

userInfoList = [i[0] + ',' + i[1] + ',' + getInfo(i[2]) for i in userInfoUrlList]
userTagList = [i[0] + ',' + i[1] + ',' + getInfo(i[2]) for i in userTagUrlList]
coAutList = [i[0] + ',' + i[1] + ',' + getInfo(i[2]) for i in coAutUrlList]
coComList = [i[0] + ',' + i[1] + ',' + getInfo(i[2]) for i in coComUrlList] 
sameDomList = [i[0] + ',' + i[1] + ',' + getInfo(i[2]) for i in sameDomUrlList]
sameOrgList = [i[0] + ',' + i[1] + ',' + getInfo(i[2]) for i in sameOrgUrlList]

with open('userInfo.txt', 'a') as fd:
  for i in userInfoList:
    fd.write(i + '\n')

with open('userTag.txt', 'a') as fd:
  for i in userTagList:
    fd.write(i + '\n')

with open("coAut.txt", 'a') as fd:
  for i in coAutList:
    fd.write(i + '\n')

with open("coCom.txt", 'a') as fd:
  for i in coComList:
    fd.write(i + '\n')

with open("sameDom.txt", 'a') as fd:
  for i in sameDomList:
    fd.write(i + '\n')

with open("sameOrg.txt", 'a') as fd:
  for i in sameOrgList:
    fd.write(i + '\n')
