#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

import xlwt

import db.mysqldb as mydb
from config import config

print('----------------------*----------------------')
print('                  导出xls文件                 ')
print('----------------------*----------------------')
db = mydb.MysqlDB(**config.get('mysqldb'))
work_book = xlwt.Workbook()
# 查询出所有的account
sql = "select __biz, account from wechat_account"
accounts = db.find(sql)
print('即将导出以下公众号的相关数据')
print('*********************************************')
for account in accounts:
    print(account[1])
print('*********************************************')

datetime_range = input('输入需要导出的日期范围'
                       '\n（格式2012-02-12 00:00:00~2020-03-07 00:00:00）'
                       '\n 如果省略其中一者则视为一端无界：').split('~')
left_bound = right_bound = None
if len(datetime_range) >= 1:
    if datetime_range[0]:
        left_bound = datetime.strptime(datetime_range[0], '%Y-%m-%d %H:%M:%S')
    if datetime_range[1]:
        right_bound = datetime.strptime(datetime_range[1], '%Y-%m-%d %H:%M:%S')

for account in accounts:
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style0 = xlwt.XFStyle()
    style0.alignment = alignment
    sheet = work_book.add_sheet(account[1], cell_overwrite_ok=True)
    sql = "select article.title,article.publish_time," \
          "dynamic.like_num,dynamic.read_num from wechat_article as article " \
          "left join wechat_article_dynamic as dynamic on article.__biz = dynamic.__biz" \
          " where article.__biz = '{__biz}'" \
        .format(__biz=account[0])

    if left_bound is not None:
        sql += " and article.publish_time >= '{}'".format(
            left_bound.strftime('%Y-%m-%d %H:%M:%S'))
    if right_bound is not None:
        sql += " and article.publish_time <= '{}'".format(
            right_bound.strftime('%Y-%m-%d %H:%M:%S'))
    print(sql)
    sheet.write_merge(0, 0, 0, 4, account[1], style0)
    heads = ('序号', '文章标题', '发布时间', '点赞量', '阅读量')
    articles = db.find(sql)
    print('正在导出公众号{}的{}篇文章数据...'.format(account[1], len(articles)))
    for i in range(0, len(heads)):
        sheet.write(1, i, heads[i], style0)
    for i in range(0, len(articles)):
        sheet.write(i + 2, 0, i + 1, style0)
        for j in range(1, len(articles[i]) + 1):
            data = articles[i][j - 1]
            if isinstance(data, datetime):
                sheet.write(i + 2, j, data.strftime('%Y年%m月%d日 %H:%M:%S'), style0)
            else:
                sheet.write(i + 2, j, data)
    sheet.col(1).width = 256 * 30
    sheet.col(2).width = 256 * 20
target = input('导出完成，选择目标目录（默认为同级目录，且保存名为当前日期）：')
work_book.save('{}.xls'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')) if target == '' else target)
