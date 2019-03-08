#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 把原始报表下载到内存中，使用pandas进行横向合并、重采样处理后，作为邮件附件发送。


import requests
import pandas as pd
from core_downloader import DailyDownloader
from core_sendmail import SendMail
from io import BytesIO
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class IODownloader(DailyDownloader):

    def download(self):
        # local_dir = self.cfg.get('local','local_dir')

        buffer = BytesIO()
        req = requests.get(self.url)
        buffer.write(req.content)
        buffer.seek(0)  #修改为python3的时候新增了这一步

        return buffer


class IOSendMail(SendMail):
    
    def makemail(self, text, attfiles):
    # 带附件的邮件实例
        mail = MIMEMultipart()
        mail['From'] = 'Robot<canon@bjceee.net.cn>'
        mail['To'] = self.to_addr
        mail['Subject'] = Header(self.subject)
        # 邮件正文
        msg = MIMEText(text, 'plain', 'utf-8')
        mail.attach(msg)
        # 附件
        for filename, df in attfiles.items():
            bio = BytesIO()
            # By setting the 'engine' in the ExcelWriter constructor.
            writer = pd.ExcelWriter(bio, engine='xlwt')
            df.to_excel(writer, sheet_name='Sheet1')
            # Save the workbook
            writer.save()
            # Seek to the beginning and read to copy the workbook to a variable in memory
            bio.seek(0)
            workbook = bio.read()
            bio.close()

            att1 = MIMEText(workbook, 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="%s"' % filename
            mail.attach(att1)
        return mail


if __name__ == '__main__':

    # 把excel表格合并成一个sheet，并且重新采样
    def excel_reform(loaders):

        attfiles = {}

        for loader in loaders:
        
            report = loader.download()
            
            sheets_list = pd.read_excel(report, sheet_name=None, index_col=0, usecols=[0,2], na_values=[0])
            
            for k ,v in sheets_list.items():
                v.rename(columns={u'值':k}, inplace=True)

            concat_df = pd.concat(sheets_list.values(), axis=1)

            res_df = concat_df.resample('5min').mean()

            attfiles[loader.filename] = res_df

        return attfiles

    # 后缀为2的json文件中的url对应的是下载含多个sheet的excel的api
    boilder_loader = IODownloader('./SXGD_Boiler2.json', './SXGD.conf')
    CDQ_loader = IODownloader('./SXGD_CDQ2.json', './SXGD.conf')
    Cyclone_loader = IODownloader('./SXGD_Cyclone2.json', './SXGD.conf')

    SXGD_loaders = [boilder_loader, CDQ_loader, Cyclone_loader]
    
    SXGD_att = excel_reform(SXGD_loaders)

    SXGD_sender = IOSendMail(u'山西光大IO DOWNLOAD TEST ON WIN py3 json',
                      u'测试信息，无需回复',
                      SXGD_att,
                      './core_config.ini')
    SXGD_sender.send()

    SDJN_boilder_loader = IODownloader('./SDJN_Boiler2.json', './SDJN.conf')
    SDJN_CDQ_loader = IODownloader('./SDJN_CDQ2.json', './SDJN.conf')

    SDJN_loaders = [SDJN_boilder_loader, SDJN_CDQ_loader]
    
    SDJN_att = excel_reform(SDJN_loaders)

    SDJN_sender = IOSendMail(u'山东金能IO DOWNLOAD TEST ON WIN py3 json',
                      u'测试信息，无需回复',
                      SDJN_att,
                      './core_config.ini')
    SDJN_sender.send()