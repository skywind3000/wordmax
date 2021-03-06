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
import ascmini

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
    if 'default' not in cfg.config:
        cfg.config['default'] = {}
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
mlog = ascmini.TraceOut(path_data('logs/m'))
mlog._makedir = True


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        print(path_data('output'))
        return 0
    def test2():
        mlog.info('hello')
        mlog.warn('hello')
        return 0
    test1()

