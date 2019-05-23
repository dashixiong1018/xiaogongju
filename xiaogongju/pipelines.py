# -*- coding: utf-8 -*-
import sqlite3
import scrapy
import datetime
from xiaogongju.spiders.doubanBook import DoubanbookSpider

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaogongjuPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):

        self.start_time = datetime.datetime.now()
        try:
            self.db_name = spider.settings.get('SQLITE_DB_NAME', 'doubanBook.db')
            self.db_conn = sqlite3.connect(self.db_name)
            self.db_cur = self.db_conn.cursor()
            self.db_conn.execute("Drop TABLE IF EXISTS %s" % DoubanbookSpider.input_tag)

            self.db_conn.execute('create table %s (title text,author text,star text'
                ',publish text,pub_time text,price varchar,jianjie text);' % DoubanbookSpider.input_tag)

        except:
            pass

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        self.end_time = datetime.datetime.now()
        print("总共耗时：%s" % str(self.end_time - self.start_time))

    def process_item(self, item, spider):


        values = (
            item['title'].replace('\n','').replace(' ',''),
            item['author'],
            item['star'].replace('\n','').replace(' ',''),
            item['publish'],
            item['pub_time'],
            item['price'],
            item['jianjie'].replace(' ',''),
        )

        sql = 'INSERT INTO %s VALUES(?,?,?,?,?,?,?)' % DoubanbookSpider.input_tag
        self.db_cur.execute(sql, values)

        return item
