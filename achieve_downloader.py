# -*- coding:utf-8 -*-

# from new_downloader import BaseDownloader
import time, datetime, requests, os, json, calendar, logging, random

class AchieveDownlaoder(object):


    def __init__(self, start_date=None, end_date=None):

        #不同于BaseDownloader，这里的start_date, end_date需要是datetime.date对象
        self.date = (start_date, end_date)


    def mk_url(self, point, *arges):
        key = 11644473600434

        start_date, end_date = self.date
        begin_time = time.mktime(datetime.datetime.combine(
            start_date, datetime.time.min).timetuple())
        end_time = time.mktime(datetime.datetime.combine(
            end_date, datetime.time.max).timetuple())
        begin_id = (int(begin_time) * 1000 + key) * 10000
        end_id = (int(end_time) * 1000 + key) * 10000

        url_head = 'http://47.94.1.242:10086/api//ExportToExcel?beginTime=%s&endTime=%s&point='

        url_body = point
        url = url_head % (begin_id, end_id) + url_body
        print(url)
        return url

    def mk_filename(self, point, *arges):
        date_str = self.date[0].strftime("%Y-%m-%d_")
        filename = date_str + point + '.xls'
        return filename

    def download(self, point, sav_dir):
        local_dir = os.path.normcase(sav_dir)

        if not os.path.exists(local_dir):
            os.mkdir(local_dir)
        
        url = self.mk_url(point)
        filename = self.mk_filename(point)

        if os.path.exists(local_dir+filename):
            print(local_dir+filename+'已存在，跳过')
            return
        # urllib.request.urlretrieve(url, local_dir + filename)

        req = requests.get(url, stream=True)

        with open(local_dir+filename, 'wb') as f:
            f.write(req.raw.read())

        print(filename)

        time.sleep(random.randint(1,4)/10)


if __name__ == "__main__":

    def get_excel(date):

        points = json.loads(open('./SXGD_all.json', encoding='utf-8').read())
        save_folder = './SXGD/' + date.strftime("%Y-%m-%d") + '/'

        downloader = AchieveDownlaoder(date, date)

        for p in points:

            downloader.download(p, save_folder)



    cal = calendar.Calendar()

    logging.basicConfig(filename='achievedownload.log',
                format='%(asctime)s:%(levelname)s:%(message)s',
                level=logging.DEBUG)

    date_list = []
    for m in range(4,5):
        days = cal.itermonthdates(year=2018, month=m)
        date_list += list(days)

    all_date = list(set(date_list))
    all_date.sort()

    for d in all_date:
        if datetime.date(2018,3,31) < d < datetime.date(2018, 5, 1):
            # get_excel(d)
            try:
                get_excel(d)
            except Exception:
                logging.exception('下载错误:')

    # get_excel(datetime.date(2018,12,25))