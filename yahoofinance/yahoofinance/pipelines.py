# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from yahoofinance.settings import DB_NAME, TABLE_NAME, DROP_TABLE

class YahoofinancePipeline(object):
    
    def __init__(self):
        self.conn = sqlite3.connect('./' + DB_NAME + '.db')
        self.cur = self.conn.cursor()
        if DROP_TABLE:
            self.cur.execute('DROP TABLE IF EXISTS ' + TABLE_NAME)
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME +
                         '''(
                         date INTEGER PRIMARY KEY,
                         open NUMERIC,
                         high NUMERIC,
                         low NUMERIC,
                         close NUMERIC,
                         volume INTEGER,
                         adjClose NUMERIC);''')
    
    def __del__(self):
        self.conn.close()
        
    def process_item(self, item, spider):
        if len(item) != 7: # avoid dividend line
            return
        self.cur.execute('INSERT INTO ' + TABLE_NAME + ' VALUES(?,?,?,?,?,?,?)',
                         (item['date'], item['open'], item['high'], item['low'], item['close'], item['volume'], item['adjClose']))
        self.conn.commit()
        return item
