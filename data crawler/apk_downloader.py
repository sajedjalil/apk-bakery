#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   File name: download_apk.py
   Author: Dawand Sulaiman
   
   Download APK files from Google Play Store with Python
   This script scraps https://apkpure.com to get the apk download link
   Make sure you have BeautifulSoup and urllib libraries
"""

from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import os
from os.path import exists

def search(query):
    res = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(query)), headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                      'Version/9.1.2 Safari/601.7.5 '
    }).text
    soup = BeautifulSoup(res, "html.parser")
    search_result = soup.find('div', {'id': 'search-res'}).find('dl', {'class': 'search-dl'})
    
    try:
        app_tag = search_result.find('p', {'class': 'search-title'}).find('a')
        download_link = 'https://apkpure.com' + app_tag['href']
        return download_link
    except:
        return None

def download(folder, app_id, link):
    os.makedirs(folder, exist_ok=True)
    res = requests.get(link + '/download?from=details', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                      'Version/9.1.2 Safari/601.7.5 '
    }).text
    soup = BeautifulSoup(res, "html.parser").find('a', {'id': 'download_link'})
    if soup['href']:
        r = requests.get(soup['href'], stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                          'Version/9.1.2 Safari/601.7.5 '
        })
        with open( os.path.join( folder, app_id + '.apk'), 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

def download_apk(folder, app_id):
    
    if exists( os.path.join(folder, app_id+'.apk')):
        print(app_id, "Already Exists!")
        return
    
    download_link = search(app_id)

    if download_link is not None:
        print('Downloading {}.apk ...'.format(download_link))
        try:
            download(folder, app_id, download_link)
            print(app_id,'Download completed!')
        except:
            print(app_id,'Could not download.')
    else:
        print(app_id,'No results')

# Test it
# download_apk('apks', 'com.google.zxing.client.android')
