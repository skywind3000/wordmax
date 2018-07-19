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

DICT_INSTANCE = None

def open_dict():
	import stardict
	db = stardict.StarDict(path_home('share/dict/dictionary.db'))
	return db

def get_dict():
	global DICT_INSTANCE
	if not DICT_INSTANCE:
		DICT_INSTANCE = open_dict()
	return DICT_INSTANCE

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
# 
#----------------------------------------------------------------------
if __name__ == '__main__':
	def test1():
		print(path_data('output'))
		return 0
	test1()

