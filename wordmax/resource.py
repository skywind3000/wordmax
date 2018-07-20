#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# resource.py - 
#
# Created by skywind on 2018/07/20
# Last Modified: 2018/07/20 23:15:58
#
#======================================================================
from __future__ import print_function
import sys
import time
import os
import config
import ascmini
import stardict
import wordbank
import wordkit


#----------------------------------------------------------------------
# ShareData
#----------------------------------------------------------------------
class ShareData (object):

	def __init__ (self):
		self._dict = None
		self._lemma = None
		self._root = None

	def dict (self):
		if self._dict is None:
			db = config.path_home('share/dict/dictionary.db')
			self._dict = stardict.StarDict(db)
		return self._dict

	def lemma (self):
		if self._lemma is None:
			fn = config.path_home('share/dict/lemma.en.txt')
			self._lemma = stardict.LemmaDB()
			self._lemma.load(fn)
		return self._lemma

	def root (self):
		if self._root is None:
			fn = config.path_home('share/dict/wordroot.txt')
			self._root = ascmini.load_config(fn)
		return self._root

	def dict_query (self, word):
		return self.dict().query(word)



#----------------------------------------------------------------------
# LocalData
#----------------------------------------------------------------------
class LocalData (object):

	def __init__ (self):
		self._bank = None
		self._skip = None
		self._init_dirs()

	def _safe_mkdir (self, dir):
		if not os.path.exists(dir):
			try:
				os.mkdir(dir)
			except:
				pass
		return True

	def _init_dirs (self):
		self._safe_mkdir(config.path_data('bank'))
		self._safe_mkdir(config.path_data('skip'))

	def bank (self):
		if self._bank is None:
			fn = config.path_data('bank/bank.db')
			self._bank = wordbank.WordBank(fn)
		return self._bank

	def skip (self):
		if self._skip is None:
			fn = config.path_data('skip')
			



#----------------------------------------------------------------------
# local
#----------------------------------------------------------------------
share = ShareData()
local = LocalData()


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
	def test1():
		print(share.dict_query('word'))
		return 0
	test1()



