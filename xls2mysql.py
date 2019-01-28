#coding:utf-8

import pymysql
from openpyxl import load_workbook
import time

class xls:
    def __init__(self, filename, index):
        try:
            self.wb = load_workbook(filename)
            self.sheets = self.wb.get_sheet_names()
            self.ws = self.wb.get_sheet_by_name(self.sheets[index])
        except IOError, e:
            print 'IOError:', e

    def rxls(self, columns):
        


xl = xls('/Users/chris/Desktop/gadmobe.xlsx', 1)
xl.rxls('A')

class db:
    def __init__(self, host='localhost', user='root', password=None, db=None, port=3306, charset='utf8'):
        '''
             pymysql.cursors.SSCursor是流式游标,迭代读取数据,否则会将数据一次性读取到内存
             也可以写成
                self.cur = pymysql.cursors.SSCursor(conn)
        '''
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset=charset)
        self.cur = self.conn.cursor(pymysql.cursors.SSCursor)

    def fetchall(self, sql, reslut='func'):
        '''
            reslut:
                func: 返回一个迭代器
                list: 返回一个list
        '''
        self.cur.execute(sql)
        if reslut == 'func':
            return self.cur
        elif reslut == 'list':
            return [res[0] for res in self.cur]
        else:
            return self.cur

