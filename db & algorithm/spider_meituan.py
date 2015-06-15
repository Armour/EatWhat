#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

'''
Read the volcabulary from shanbay.com
'''

import cookielib, urllib2, urllib, Cookie, re, time, argparse, gzip, StringIO
from os import path
from bs4 import BeautifulSoup as bs
from IPython import embed
try:
    import json
except ImportError:
    import simplejson as json

cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
headers = {
    'Host': 'waimai.meituan.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'Referer': 'http://waimai.meituan.com/home/wtmkkvch54ej',
    'Accept-Encoding': 'deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control' : 'max-age=0',
    'Cookie': 'w_uuid=2648a519-0303-4a0b-b90d-53993e75a0b9; wm_poi_sp_area_id=39208; cookie_address="%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6%E7%B4%AB%E9%87%91%E6%B8%AF%E6%A0%A1%E5%8C%BA%E7%A2%A7%E5%B3%B03%E8%88%8D403%E5%AE%A4"; cookie_phone=18868111526; cookie_name=; tel_or_cornet=; w_h=9468|; _ga=GA1.2.981190787.1415713257; w_cid=330100; w_cpy_cn="%E6%9D%AD%E5%B7%9E"; w_cpy=hangzhou; waddrname="%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6%28%E7%B4%AB%E9%87%91%E6%B8%AF%E6%A0%A1%E5%8C%BA%29"; w_geoid=wtmkkvch54ej; w_ah="30.31060690060258,120.09305879473686,%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6%28%E7%B4%AB%E9%87%91%E6%B8%AF%E6%A0%A1%E5%8C%BA%29|30.31060690060258,120.09305879473686,%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6%E7%B4%AB%E9%87%91%E6%B8%AF%E6%A0%A1%E5%8C%BA"; _gat=1; w_utmz="utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_visitid=874d0c84-bfa1-4eda-935a-ef1a753b1f40; JSESSIONID=1hcg5tjty7hwv1c1jqmqjw1diz; _ga=GA1.3.981190787.1415713257; __mta=255636023.1433863034117.1433863706468.1433863728773.3'
}
#opener.handle_open["http"][0].set_http_debuglevel(1)

def getResponse(url, data={}, method=lambda: 'GET', **kw):
    jsdata = json.dumps(data)
    encodejsdata = urllib.urlencode(data)
    request = urllib2.Request(url, encodejsdata)
    request.get_method = method
    for name, values in headers.items():
        if name not in kw:
            request.add_header(name, values)
    for name, values in kw.items():
        request.add_header(name, values)
    response = opener.open(request, timeout = 60)
    if response.info().get('Content-Encoding') == 'gzip': # gzip
        content = response.read()
        data    = StringIO.StringIO(content)
        gzipper = gzip.GzipFile(fileobj=data)
        html    = gzipper.read()
    else: # normal page
        html = response.read()
    return html

def info(rid):
    L = {}
    url = 'http://waimai.meituan.com/restaurant/' + str(rid)
    try:
        response = getResponse(url)
    except Exception, e:
        print 'ERR: searchUser', e, url
        return
    html = bs(response, from_encoding="UTF-8")
    L = html.find_all('div', class_='j-text-food text-food clearfix')
    ans = list()
    for item in L:
        item = L[0]
        scp = item.find('script', id='foodcontext-'+item['id']).text
        dic = json.loads(scp)
        desc = item.find('div', class_='desc ct-lightgrey')
        if desc is not None:
            dic['desc'] = desc['title']
        ans.append(dic)
    return ans

def search():
    url = 'http://waimai.meituan.com/home/wtmkkvch54ej'
    try:
        response = getResponse(url)
    except Exception, e:
        print 'ERR: searchUser', e, url
        return
    html = bs(response, from_encoding="UTF-8")
    L = html.find_all('li', class_='fl rest-li')
    answer = list()
    info(6877)
    for item in L:
        try:
            tmp = dict()
            it = item.find('div', class_='restaurant')
            tmp['bulletin'] = it['data-bulletin']
            tmp['name'] = it['data-title']
            tmp['rid'] = it['data-poiid']
            tmp['score'] = item.find('span', class_='score-num fl').text
            tmp['total'] = item.find('span', class_='total').text
            tmp['list'] = info(tmp['rid'])
            answer.append(tmp)
        except Exception, e:
            pass
    print json.dumps(answer)

if (__name__ == '__main__'):
    search()
