#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# wordbook.py - 
#
# Created by skywind on 2018/07/19
# Last Modified: 2018/07/19 20:30:52
#
#======================================================================
from __future__ import print_function
import sys
import time
import os
import io
import sqlite3

try:
	import json
except:
	import simplejson as json

MySQLdb = None


#----------------------------------------------------------------------
# python3 compatible
#----------------------------------------------------------------------
if sys.version_info[0] >= 3:
	unicode = str
	long = int
	xrange = range



#----------------------------------------------------------------------
# WordBook
#----------------------------------------------------------------------
class WordBook (object):

	def __init__ (self, filename, verbose = False):
		self.__dbname = os.path.abspath(filename)
		self.__conn = None
		self.__verbose = verbose
		self.__open()

	def __open(self):
		sql = '''
		CREATE TABLE IF NOT EXISTS "wordbook" (
			"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
			"word" VARCHAR(64) COLLATE NOCASE NOT NULL UNIQUE,
			"mode" INTEGER DEFAULT(0),
			"score" INTEGER DEFAULT(0),
			"atime" DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
			"mtime" DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
			"ctime" DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
		);
		CREATE UNIQUE INDEX IF NOT EXISTS "wordbook_1" ON wordbook (id);
		CREATE UNIQUE INDEX IF NOT EXISTS "wordbook_2" ON wordbook (word);
		CREATE INDEX IF NOT EXISTS "wordbook_3" ON wordbook (mode);
		CREATE INDEX IF NOT EXISTS "wordbook_4" ON wordbook (atime);
		'''
		
		self.__conn = sqlite3.connect(self.__dbname, isolation_level = 'IMMEDIATE')
		self.__conn.isolation_level = 'IMMEDIATE'

		sql = '\n'.join([ n.strip('\t') for n in sql.split('\n') ])
		sql = sql.strip('\n')

		self.__conn.executescript(sql)
		self.__conn.commit()

		fields = ( 'id', 'word', 'mode', 'score', 'atime', 'mtime', 'ctime' )
		self.__fields = tuple([(fields[i], i) for i in range(len(fields))])
		self.__names = {}
		for k, v in self.__fields:
			self.__names[k] = v

		self.__enable = self.__fields[2:-1]

		return True

	def __record2obj (self, record):
		if record is None:
			return None
		word = {}
		for k, v in self.__fields:
			word[k] = record[v]
		return word

	# 关闭数据库
	def close (self):
		if self.__conn:
			self.__conn.close()
		self.__conn = None
	
	def __del__ (self):
		self.close()

	# 输出日志
	def out (self, text):
		if self.__verbose:
			print(text)
		return True

	# 查询单词
	def lookup (self, key, mode = None):
		c = self.__conn.cursor()
		record = None
		if isinstance(key, int) or isinstance(key, long):
			if mode is None:
				c.execute('select * from wordbook where id = ?;', (key,))
			else:
				c.execute('select * from wordbook where id = ? and mode = ?;', (key, mode))
		elif isinstance(key, str) or isinstance(key, unicode):
			if mode is None:
				c.execute('select * from wordbook where word = ?', (key,))
			else:
				c.execute('select * from wordbook where word = ? and mode = ?;', (key, mode))
		else:
			return None
		record = c.fetchone()
		return self.__record2obj(record)

	# 取得单词总数
	def count (self, mode = None):
		c = self.__conn.cursor()
		if mode is None:
			c.execute('select count(*) from wordbook;')
		else:
			c.execute('select count(*) from wordbook where mode = ?;', (mode,))
		record = c.fetchone()
		return record[0]

	# 注册新单词
	def register (self, word, items, commit = True):
		sql = 'INSERT INTO wordbook(word, ctime) VALUES(?, Now())'
		try:
			self.__conn.execute(sql, (word,))
		except sqlite3.IntegrityError as e:
			self.out(str(e))
			return False
		except sqlite3.Error as e:
			self.out(str(e))
			return False
		self.update(word, items, commit)
		return True

	# 删除单词
	def remove (self, key, commit = True):
		if isinstance(key, int) or isinstance(key, long):
			sql = 'DELETE FROM wordbook WHERE id=?;'
		else:
			sql = 'DELETE FROM wordbook WHERE word=?;'
		try:
			self.__conn.execute(sql, (key,))
			if commit:
				self.__conn.commit()
		except sqlite3.IntegrityError:
			return False
		return True

	# 更新单词数据
	def update (self, key, items, commit = True):
		names = []
		values = []
		for name, id in self.__enable:
			if name in items:
				names.append(name)
				value = items[name]
				values.append(value)
		if len(names) == 0:
			if commit:
				try:
					self.__conn.commit()
				except sqlite3.IntegrityError:
					return False
			return False
		sql = 'UPDATE wordbook SET ' + ', '.join(['%s=?'%n for n in names])
		if isinstance(key, str) or isinstance(key, unicode):
			sql += ' WHERE word=?;'
		else:
			sql += ' WHERE id=?;'
		try:
			self.__conn.execute(sql, tuple(values + [key]))
			if commit:
				self.__conn.commit()
		except sqlite3.IntegrityError:
			return False
		return True

	# 选择单词
	def select (self, mode):
		c = self.__conn.cursor()
		sql = 'select "id", "word" from "wordbook"'
		sql += ' WHERE mode = ?'
		sql += ' order by "atime";'
		c.execute(sql, (mode,))
		return c.__iter__()

	# 按照时间区域选择
	def select_atime (mode, since = None, to = None):
		return c.__iter__()

	# 浏览词典
	def __iter__ (self):
		c = self.__conn.cursor()
		sql = 'select "id", "word" from "wordbook"'
		sql += ' order by "atime";'
		c.execute(sql)
		return c.__iter__()

	# 取得长度
	def __len__ (self):
		return self.count()

	# 检测存在
	def __contains__ (self, key):
		return self.query(key) is not None

	# 查询单词
	def __getitem__ (self, key):
		return self.query(key)

	# 提交变更
	def commit (self):
		try:
			self.__conn.commit()
		except sqlite3.IntegrityError:
			self.__conn.rollback()
			return False
		return True

	# 取得所有单词
	def dumps (self):
		return [ n for _, n in self.__iter__() ]




#----------------------------------------------------------------------
# testing case 
#----------------------------------------------------------------------
if __name__ == '__main__':
	def test1():
		ws = WordBook("test.db")
		return 0
	test1()

