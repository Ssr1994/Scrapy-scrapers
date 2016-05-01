# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from keywordsearch.settings import DB_NAME, TABLE_NAME, DROP_TABLE

class KeywordsearchPipeline(object):
    
    def __init__(self):
        self.conn = sqlite3.connect('./' + DB_NAME + '.db')
        self.cur = self.conn.cursor()
        if DROP_TABLE:
            self.cur.execute('DROP TABLE IF EXISTS ' + TABLE_NAME)
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NAME +
                         '''(
                         title TEXT,
                         author TEXT,
                         keyline TEXT,
                         time TEXT,
                         publisher TEXT,
                         url TEXT,
                         query TEXT,
                         content TEXT);''')
    
    def __del__(self):
        self.conn.close()
        
    def process_item(self, item, spider):
        for k, v in item.iteritems():
            if isinstance(v, list):
                item[k] = ''.join(v)
        self.cur.execute('INSERT INTO ' + TABLE_NAME + ' VALUES(?,?,?,?,?,?,?,?)',
                         (item['title'], item['author'], item['keyLine'], item['time'], item['publisher'], item['url'], item['query'], item['content']))
        self.conn.commit()
        return item
