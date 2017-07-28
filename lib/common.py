#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160518

"""
* Author Dave
* Version 1.0
* 此文件中包含的方法属于常用方法，一些复用多的方法。
"""


def normalize_url(target, https=False):
    # 标准化 Target 信息
    if not target:
        return
    elif target.startswith(('http://', 'https://')):
        return target
    if not https:
        target = 'http://' + target
    else:
        target = 'https://' + target
    return target
