#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# wordkit.py - 
#
# Created by skywind on 2018/07/20
# Last Modified: 2018/07/20 16:18:34
#
#======================================================================
from __future__ import print_function, unicode_literals
import sys
import time
import os
import codecs


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

    def __init__ (self, filename = None):
        self._words = []
        self._lookup = {}
        self._info = {}
        self._title = None
        self._count = 0
        self.load(filename)

    def reset (self):
        self._words = []
        self._lookup = {}
        self._title = None
        self._count = 0

    def push (self, word, info = None):
        word = word.strip('\r\n\t ')
        if not word:
            return False
        key = word.lower()
        if key in self._lookup:
            return False
        self._lookup[key] = len(self._words)
        self._words.append(word)
        self._info[key] = info
        self._count = len(self._words)
        return True
    
    def load (self, filename):
        if filename is None:
            return False
        if isinstance(filename, str) or isinstance(filename, unicode):
            fp = open(filename, 'r')
        else:
            fp = filename
        for line in fp:
            line = line.strip('\r\n\t ')
            if not line: 
                continue
            if line.startswith('#') or line.startswith(';'):
                line = line[1:].lstrip('\r\n\t ')
                if line and self._title is None:
                    self._title = line
                continue
            word, _, info = line.partition(',')
            word = word.strip()
            if not word:
                continue
            info = info.strip()
            if info:
                info = info.split(',')
            else:
                info = None
            self.push(word, info)
        fp.close()
        return True

    def check (self, key):
        return self._lookup.__contains__(key.lower())
    
    def __contains__ (self, key):
        return self._lookup.__contains__(key.lower())

    def __len__ (self):
        return self._count

    def __getitem__ (self, key, default = None):
        if isinstance(key, unicode) or isinstance(key, str):
            return self._lookup.get(key.lower(), default)
        if key < 0 or key >= self._count:
            return default
        return self._words[key]

    def __iter__ (self):
        return self._words.__iter__()

    def info (self, key):
        return self._info.get(key.lower())

    def minus (self, wb):
        result = []
        for word in self._words:
            if word not in wb:
                result.append(word)
        return result

    def dumps (self):
        return [ n for n in self._words ]


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        wb = WordBook('e:/english/english/skip/simple-1.txt')
        wb.load('e:/english/english/skip/simple-2.txt')
        print(len(wb))
        return 0
    test1()



