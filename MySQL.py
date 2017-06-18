#!/usr/bin/python
# coding:utf-8
import mysql.connector


class MySQL:
    def __init__(self, db=None):
        if db is None:
            self.database = db
        else:
            self.database = 'booklist'
        self.user = 'root'
        self.password = 'meiyoumima'
        self.port = '3306'
        self.encode = 'utf-8'
        self.host = 'localhost'
        self.conn = self.getConnect()

    def getConnect(self):
        try:
            return mysql.connector.connect(host=self.host, user=self.user,
                                           password=self.password, database=self.database)
        except mysql.connector.Error as e:
            print(str(e))

    def query(self, sql):
        if self.conn is None:
            print('no connection')
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(str(e))
            return None

    def insert(self, key, value, table):
        sql = self.getSql(key, value, table)
        try:
            cursor = self.conn.cursor()
            result = cursor.execute(sql, value)
            row = cursor.rowcount
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as e:
            print(e)
        pass

    def getSql(self, keys, values, table):
        if keys is None or values is None:
            return

        if table is None:
            return

        if len(keys) != len(values):
            print('keys not equals to value')
            return

        keyStr = keys[0]
        valueStr = '%s'
        for x in range(1, len(keys)):
            keyStr = keyStr + ', ' + keys[x]
            valueStr = valueStr + ', ' + '%s'
        sql = 'insert into ' + table + ' (' + keyStr + ')' + ' values (' + valueStr + ')'

        return sql

# conn = MySQL('booklist')
# keys = ['name', 'subtitle', 'img', 'author', 'publish', 'publish_year', 'price', 'binding', 'isbn', 'average', 'page_num', 'catalog', 'author_introduction',  'content_introduction']
# values = ['name', 'subtitle', 'img', 'author', 'publish', '2', '1', 'binding', '111111', '1', '1', 'catalog', 'author_introduction',  'content_introduction']
# conn.insert(keys,values,'book')
# #
# # keys = ['k']
# # values = ['1']
# # conn.insert(keys, values, 'test')
# pass
