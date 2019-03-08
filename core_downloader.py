#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 20180806改为使用python3,主要区别在于urllib中一些方法的层级，
# print的写法，字符串处理相关，configparser模块名称变成小写
# 20180807改成使用json存储本地信息

import urllib
import time
import datetime
import requests
import json
import os
from configparser import SafeConfigParser
# from io import BytesIO


class DailyDownloader(object):
    def __init__(self, json_file, cfg_file):
        self.cfg = SafeConfigParser()
        self.cfg.read(cfg_file, encoding='utf-8')
        self.date = datetime.date.today() + datetime.timedelta(days=-1)  # 获取昨天的日期
        self.load_info = json.load(open(json_file, 'r', encoding='utf-8'))
        self.url = self.makeurl()
        self.filename = self.makefilename()

    def download(self):
        local_dir = self.cfg.get('local', 'local_dir')
        local_dir = os.path.normcase(local_dir)
        urllib.request.urlretrieve(self.url, local_dir + self.filename)

    def makeurl(self):
        key = 11644473600434
        begin_time = time.mktime(datetime.datetime.combine(
            self.date, datetime.time.min).timetuple())
        end_time = time.mktime(datetime.datetime.combine(
            self.date, datetime.time.max).timetuple())
        begin_id = (int(begin_time) * 1000 + key) * 10000
        end_id = (int(end_time) * 1000 + key) * 10000

        proj_head = self.cfg.get('local', 'proj_head')

        url_body = ';'.join(proj_head + urllib.request.quote(line)
                            for line in self.load_info['url_body'])
        url = self.load_info['url_head'] % (begin_id, end_id) + url_body
        print(url)
        return url

    def makefilename(self):
        date_str = self.date.strftime("%Y-%m-%d")
        filename = date_str + self.load_info['device'] + '.xls'
        return filename


class ManualDownloader(DailyDownloader):
    def __init__(self, json_file, cfg_file):
        super(ManualDownloader, self).__init__(json_file, cfg_file)
        y, m, d = input('Input date like \'yyyy, m, d\': ')
        self.date = datetime.date(y, m, d)
        self.load_info = json.load(open(json_file, 'r', encoding='utf-8'))
        self.url = self.makeurl()
        self.filename = self.makefilename()


if __name__ == '__main__':
    CDQdownloader = DailyDownloader(
        './SDJN_CDQ2.json', './SDJN.conf')
    CDQdownloader.download()
    
    Boilerdownloader = DailyDownloader(
        './SDJN_Boiler2.json', './SDJN.conf')
    Boilerdownloader.download()
    #
    # Cyclonedownloader = DailyDownloader('SXGD_Cyclone.txt', 'Cyclone')
    # Cyclonedownloader.download()
    #
    # Cyclonedownloader = ManualDownloader('SXGD_Cyclone.txt', 'Cyclone')
    # Cyclonedownloader.download()
    #
    # CDQdownloader = ManualDownloader('SXGD_CDQ.txt', 'CDQ')
    # CDQdownloader.download()
    #
    # Boilerdownloader = ManualDownloader('SXGD_Boiler.txt', 'Boiler')
    # Boilerdownloader.download()
