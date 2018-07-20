#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# config.py - configuration
#
# Created by skywind on 2018/06/18
# Last Modified: 2018/06/18 21:36:14
#
#======================================================================
from __future__ import print_function
import sys
import os

LIBHOME = os.path.dirname(os.path.abspath(__file__))
DIRHOME = os.path.abspath(os.path.join(LIBHOME, '..'))

# 取得子目录权限
def path_home(name):
	return os.path.abspath(os.path.join(DIRHOME, name))

sys.path.append(LIBHOME)

def load_config():
	import ascmini
	cfgname = os.path.expanduser('~/.config/wordmax/wordmax.ini')
	cfgname = os.path.abspath(cfgname)
	cfg = ascmini.ConfigReader(cfgname)
	if 'data' not in cfg.config['default']:
		data = os.path.expanduser('~/.cache/wordmax')
		data = os.path.abspath(data)
		cfg.config['default']['data'] = data
	return cfg

cfg = load_config()

# 取得数据文件目录
DATHOME = cfg.option('default', 'data')

# 如果不存在则创建数据目录
if not os.path.exists(DATHOME):
	os.makedirs(DATHOME)

# 取得数据文件目录内的路径
def path_data(name):
	return os.path.abspath(os.path.join(DATHOME, name))


#----------------------------------------------------------------------
# 日志模块
#----------------------------------------------------------------------
class MyLog (object):
	def __init__ (self):
		self.home = path_data('logs')
		import ascmini
		self.mlog = ascmini.TraceOut(self.home + '/m')
		self.init = False
	def __init (self):
		if self.init:
			return True
		if not os.path.exists(self.home):
			try:
				os.mkdir(self.home)
			except:
				pass
		self.init = True
		return True
	def out (self, channel, *args):
		


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
	def test1():
		print(path_data('output'))
		return 0
	test1()

