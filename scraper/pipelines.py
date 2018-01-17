# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import traceback


class ScraperPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='scrapy',
            charset="utf8",
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """INSERT INTO currency 
                (name, symbol, marketcap, price, circulatingsupply, volume, percent_1h, percent_24h, percent_7d) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    item['Name'], item['Symbol'],
                    item['MarketCap'], item['Price'],
                    item['CirculatingSupply'], item['Volume'],
                    item['Percent_1h'], item['Percent_24h'],
                    item['Percent_7d']
                )
            )

            self.conn.commit()

        except MySQLdb.Error, e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

        return item
