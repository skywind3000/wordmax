#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# config.py - 
#
# Created by skywind on 2019/10/30
# Last Modified: 2019/10/30 17:37:26
#
#======================================================================
from __future__ import print_function, unicode_literals
import sys
import os

HOME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lib')
HOME = os.path.normpath(HOME)

sys.path.append(HOME)


#----------------------------------------------------------------------
# YCM/Jedi Hints
#----------------------------------------------------------------------
if False:
    sys.path.append('../lib')

import ascmini
import ccinit


#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        return 0
    test1()


