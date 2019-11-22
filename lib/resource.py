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
        self._todo = None
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

    def todo (self):
        if self._todo is None:
            base = ccinit.path_data('todo')
            self._todo = wordkit.WordBook()
            for fn in os.listdir(base):
                if os.path.splitext(fn)[-1].lower() == '.txt':
                    fn = os.path.join(base, fn)
                    self._todo.load(fn)
        return self._todo
            
    def skip_simple (self, word):
        if "'" in word:
            return True
        skip = self.skip()
        return skip.check(word)

    def skip_todo (self, word):
        if "'" in word:
            return True
        todo = self.todo()
        return todo.check(word)

    def bank_query (self, word):
        bank = self.bank()
        return bank.query(word)


#----------------------------------------------------------------------
# local
#----------------------------------------------------------------------
share = ShareData()
local = LocalData()


#----------------------------------------------------------------------
# tools
#----------------------------------------------------------------------
class ToolBox (object):

    def __init__ (self):
        self._tts_engine = None  

    def audio_locate (self):
        locate = ccinit.cfg.option('default', 'audio')
        if not locate:
            locate = ccinit.path_home('share/audio')
        return locate

    def audio_play (self, word, volume = None, wait = True):
        if sys.platform[:3] != 'win':
            return False
        locate = self.audio_locate()
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

    def audio_stop (self):
        if sys.platform[:3] != 'win':
            return False
        import playmp3
        return playmp3.audio_stop()

    def audio_check (self):
        if sys.platform[:3] != 'win':
            return False
        import playmp3
        return playmp3.audio_check()

    def tts_engine (self):
        if not self._tts_engine:
            try:
                import pyttsx3
            except ImportError:
                return None
            self._tts_engine = pyttsx3.init()
            voices = self._tts_engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    self._tts_engine.setProperty('voice', voice.id)
                    # print('choose: %s'%voice.name)
                    break
        return self._tts_engine

    def tts_say (self, text):
        engine = self.tts_engine()
        if not engine:
            return False
        engine.say(text)
        engine.runAndWait()
        return True

    def disorder (self, array):
        import random
        b = [ n for n in array ]
        n = []
        while len(b) > 0:
            i = random.randint(0, len(b) - 1)
            n.append(b[i])
            b[i] = b[len(b) - 1]
            b.pop()
        return n

    def say (self, word):
        hr = self.audio_play(word)
        if not hr:
            return self.tts_say(word)
        return True

    def word_frq (self, word):
        q = share.dict_query(word)
        if not q:
            return None
        elif (not q['frq']) and (not q['bnc']):
            return None
        if q['frq'] and (not q['bnc']):
            frq = q['frq']
        elif (not q['frq']) and q['bnc']:
            frq = q['bnc']
        elif q['frq'] and q['bnc']:
            frq = min(q['frq'], q['bnc'])
        else:
            raise ValueError('word frq error: %s'%word)
        return frq

    def importance (self, word):
        if local.skip_simple(word):
            return False
        q = share.dict_query(word)
        if not q:
            return False
        if not q['frq']:
            return False
        elif not q['bnc']:
            return False
        if self.word_frq(word) > 20000:
            return False
        return True

    def word_score (self, word):
        q = share.dict_query(word)
        if not q:
            return 0
        detail = q['detail']
        if q['oxford'] == 1:
            if 'zk' in q['tag']:
                return 0
            elif 'gk' in q['tag']:
                return 1
            return 2
        frq = self.word_frq(word)
        if frq is None:
            return None
        if frq < 3000:
            return 2
        elif frq < 4000:
            return 3
        elif frq >= 4000 and frq <= 20000:
            level = int((frq - 4000) // 1000)
            return 4 + level
        return None

    def save_list (self, filename, words):
        if isinstance(words, dict):
            input = []
            for word in words:
                input.append((word, words[word]))
            words = input
        with open(filename, 'w') as fp:
            count = 0
            for item in words:
                if isinstance(item, str):
                    word = item
                    fp.write('%s\n'%word)
                elif isinstance(item, list) or isinstance(item, tuple):
                    part = [ str(n) for n in item ]
                    if len(part) < 1:
                        continue
                    fp.write((', '.join(part)) + '\n')
                count += 1
                if count >= 10:
                    count = 0
                    fp.write('\n')
        return 0


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
utils = ToolBox()


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
        utils.audio_play('hello')
        return 0
    def test3():
        utils.tts_say('I will speak this text')
        return 0
    test3()



