#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# wordbank.py - 
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
import datetime
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
# WordBank
#----------------------------------------------------------------------
class WordBank (object):

	def __init__ (self, filename, verbose = False):
		self.__dbname = os.path.abspath(filename)
		self.__conn = None
		self.__verbose = verbose
		self.__open()

	def __open(self):
		sql = '''
		CREATE TABLE IF NOT EXISTS "wordbank" (
			"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
			"word" VARCHAR(64) COLLATE NOCASE NOT NULL UNIQUE,
			"mode" INTEGER DEFAULT(0),
			"score" INTEGER DEFAULT(0),
			"atime" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			"mtime" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
			"ctime" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
		);
		CREATE UNIQUE INDEX IF NOT EXISTS "wordbank_1" ON wordbank (id);
		CREATE UNIQUE INDEX IF NOT EXISTS "wordbank_2" ON wordbank (word);
		CREATE INDEX IF NOT EXISTS "wordbank_3" ON wordbank (mode);
		CREATE INDEX IF NOT EXISTS "wordbank_4" ON wordbank (atime);
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
				c.execute('select * from wordbank where id = ?;', (key,))
			else:
				c.execute('select * from wordbank where id = ? and mode = ?;', (key, mode))
		elif isinstance(key, str) or isinstance(key, unicode):
			if mode is None:
				c.execute('select * from wordbank where word = ?', (key,))
			else:
				c.execute('select * from wordbank where word = ? and mode = ?;', (key, mode))
		else:
			return None
		record = c.fetchone()
		return self.__record2obj(record)

	# 取得单词总数
	def count (self, mode = None):
		c = self.__conn.cursor()
		if mode is None:
			c.execute('select count(*) from wordbank;')
		else:
			c.execute('select count(*) from wordbank where mode = ?;', (mode,))
		record = c.fetchone()
		return record[0]

	# 注册新单词
	def register (self, word, items, commit = True):
		sql = 'INSERT INTO wordbank(word) VALUES(?)'
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
			sql = 'DELETE FROM wordbank WHERE id=?;'
		else:
			sql = 'DELETE FROM wordbank WHERE word=?;'
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
		sql = 'UPDATE wordbank SET ' + ', '.join(['%s=?'%n for n in names])
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
		sql = 'select "id", "word" from "wordbank"'
		sql += ' WHERE mode = ?'
		sql += ' order by "id";'
		c.execute(sql, (mode,))
		return c.__iter__()

	# 按照时间区域选择
	def select_atime (self, mode, since = None, to = None):
		c = self.__conn.cursor()
		sql = 'select "id", "word" from "wordbank"'
		name = ['mode = ?']
		cond = [mode]
		if since is not None:
			name.append('atime >= ?')
			cond.append(since)
		if to is not None:
			name.append('atime < ?')
			cond.append(to)
		sql += ' WHERE ' + ' and '.join(name)
		sql += ' order by "atime";'
		c.execute(sql, tuple(cond))
		return c.__iter__()

	# 按照时间区域选择
	def select_mtime (self, mode, since = None, to = None):
		c = self.__conn.cursor()
		sql = 'select "id", "word" from "wordbank"'
		name = ['mode = ?']
		cond = [mode]
		if since is not None:
			name.append('mtime >= ?')
			cond.append(since)
		if to is not None:
			name.append('mtime < ?')
			cond.append(to)
		sql += ' WHERE ' + ' and '.join(name)
		sql += ' order by "mtime";'
		c.execute(sql, tuple(cond))
		return c.__iter__()

	# 清空数据库
	def delete_all (self, reset_id = False):
		sql1 = 'DELETE FROM wordbank;'
		sql2 = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'wordbank';"
		try:
			self.__conn.execute(sql1)
			if reset_id:
				self.__conn.execute(sql2)
			self.__conn.commit()
		except sqlite3.IntegrityError as e:
			self.out(str(e))
			return False
		except sqlite3.Error as e:
			self.out(str(e))
			return False
		return True

	# 浏览词典
	def __iter__ (self):
		c = self.__conn.cursor()
		sql = 'select "id", "word" from "wordbank"'
		sql += ' order by "id";'
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

	# 移动单词
	def move (self, key, mode, commit = True):
		update = {}
		current = time.strftime('%Y-%m-%d %H:%M:%S')
		update['mode'] = mode
		update['score'] = 0
		update['mtime'] = current
		update['atime'] = current
		return self.update(key, update, commit)

	# 取得所有单词
	def dumps (self, mode):
		return [ n for _, n in self.select(mode) ]




#----------------------------------------------------------------------
# testing case 
#----------------------------------------------------------------------
if __name__ == '__main__':
	def test1():
		ws = WordBank("test.db")
		ws.delete_all()
		ws.register('fuck', {})
		ws.register('you', {})
		ws.register('asshole', {})
		ws.move('asshole', 2)
		print(ws.dumps(0))
		print(ws.lookup('you'))
		return 0
	test1()


