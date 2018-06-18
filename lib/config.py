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
def path(name):
	return os.path.abspath(os.path.join(DIRHOME, name))

sys.path.append(LIBHOME)

DICT_INSTANCE = None

def open_dict():
	import stardict
	db = stardict.StarDict(path('share/dict/dictionary.db'))
	return db

def get_dict():
	global DICT_INSTANCE
	if not DICT_INSTANCE:
		DICT_INSTANCE = open_dict()
	return DICT_INSTANCE


