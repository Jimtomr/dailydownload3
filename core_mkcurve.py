#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 20180806改为使用python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from configparser import SafeConfigParser
import os
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class AutoMaker(object):
    def __init__(self, filename, data_id, cfg_file):
        self.cfg = SafeConfigParser()
        self.cfg.read(cfg_file, encoding='utf-8')
        self.filename = filename
        self.data_id = data_id

    def draw(self, title = u'BE3_CDQ_Project'):
        local_dir = self.cfg.get('local','local_dir')
        data = pd.read_excel(local_dir + self.filename)
        time_label = data.columns[0]
        data_res = data.set_index(time_label, drop=True).replace(0, np.nan).resample('5t').mean()
        date = data[time_label][1].strftime("%Y-%m-%d")
        for d in self.data_id:
            column_label = data.columns[d]
            fig = plt.figure(facecolor='white')
            ax = fig.add_subplot(1, 1, 1, facecolor='white')
            fig.set_size_inches(16, 10)
            ax.plot(data[time_label], [data[column_label].mean()] * len(data[column_label]),
                    label=u'平均值',
                    color='r',
                    linestyle='dotted',
                    linewidth=1,
                    alpha=1)
            data_res.plot(y=column_label,
                      label=column_label.split('.')[1] ,
                      color='#1E90FF',
                      linestyle='solid',
                      linewidth=2,
                      alpha=1,
                      ax=ax)
            # ax.annotate('max', xytext=('1','2'),xy=(xtime[???, data[d].max()))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))
            ax.xaxis.set_major_locator(mdates.HourLocator([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]))
            # ax.xaxis.grid(True)
            ax.yaxis.grid(True)
            ax.spines['bottom'].set_linewidth(1.5)
            ax.spines['top'].set_linewidth(0)
            ax.spines['left'].set_linewidth(1.5)
            ax.spines['right'].set_linewidth(0)
            ax.set_title(title + '\n' + date, fontsize=20)
            ax.legend(loc='best')
            savedir = local_dir + date + u'曲线'
            if not os.path.exists(savedir):
                os.makedirs(savedir)
            savename = savedir + '\\' + date + ' ' + column_label.split('.')[1]  + '.pdf'
            print(savename)
            fig.savefig(savename, facecolor=fig.get_facecolor(), dpi=300, bbok_inches='tight')
            # plt.show()
            plt.close(fig)


if __name__ == '__main__':
    sourcefile = '2018-08-06CDQ.xls'
    label_id = [1,3,5,7,9]
    maker = AutoMaker(sourcefile, label_id,'.\\core_config.ini')
    maker.draw(title=u'项目标题')