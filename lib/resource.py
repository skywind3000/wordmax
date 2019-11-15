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
import ccinit
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
        self._scope = None
        self._books = {}

    def dictionary (self):
        if self._dict is None:
            db = ccinit.path_home('share/dict/dictionary.db')
            self._dict = stardict.StarDict(db)
        return self._dict

    def lemma (self):
        if self._lemma is None:
            fn = ccinit.path_home('share/dict/lemma.en.txt')
            self._lemma = stardict.LemmaDB()
            self._lemma.load(fn)
        return self._lemma

    def root (self):
        if self._root is None:
            fn = ccinit.path_home('share/dict/wordroot.txt')
            self._root = ascmini.load_config(fn)
        return self._root

    def book (self, name):
        if name not in self._books:
            fn = ccinit.path_home('share/wordbook/%s'%name)
            if not os.path.exists(fn):
                return None
            book = wordkit.WordBook(fn)
            self._books[name] = book
        return self._books[name]

    def dict_query (self, word):
        return self.dictionary().query(word)

    def scope (self):
        if self._scope is None:
            fn = ccinit.path_home('share/level/scope.txt')
            self._scope = wordkit.WordBook(fn)
        return self._scope

    def scope_check (self, word):
        scope = self.scope()
        return (word in scope)


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
        self._safe_mkdir(ccinit.path_data('bank'))
        self._safe_mkdir(ccinit.path_data('skip'))

    def bank (self):
        if self._bank is None:
            fn = ccinit.path_data('bank/bank.db')
            self._bank = wordbank.WordBank(fn)
        return self._bank

    def skip (self):
        if self._skip is None:
            base = ccinit.path_data('skip')
            self._skip = wordkit.WordBook()
            for fn in os.listdir(base):
                if os.path.splitext(fn)[-1].lower() == '.txt':
                    fn = os.path.join(base, fn)
                    self._skip.load(fn)
        return self._skip
            
    def skip_simple (self, word):
        if "'" in word:
            return True
        skip = self.skip()
        return skip.check(word)

    def bank_query (self, word):
        bank = self.bank()
        return bank.query(word)


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def audio_locate():
    locate = ccinit.cfg.option('default', 'audio')
    if not locate:
        locate = ccinit.path_home('share/audio')
    return locate

def audio_play(word, volume = None, wait = True):
    if sys.platform[:3] != 'win':
        return False
    locate = audio_locate()
    if not os.path.exists(locate):
        return False
    head = word[:1].lower()
    if not head.isalnum():
        head = '-'
    src = os.path.join(locate, head, word.lower() + '.mp3')
    if not os.path.exists(src):
        return False
    import playmp3
    return playmp3.audio_play(src, volume, wait)

def audio_stop():
    if sys.platform[:3] != 'win':
        return False
    import playmp3
    return playmp3.audio_stop()


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
        print(local.skip_simple('you'))
        print(local.skip()._count)
        return 0
    def test2():
        # ccinit.cfg.config['default']['audio'] = 'e:/english/resource/audio'
        audio_play('hello')
        return 0
    test1()



