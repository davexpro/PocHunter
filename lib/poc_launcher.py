#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160518

from frame.beebeeto import Beebeeto
from frame.kspoc import KsPoc
from frame.pocsuite import PocSuite
from frame.tangscan import TangScan
from lib.common import *

"""
* Author Dave
* Version 1.0
* 此文件中包含的类用于不同平台的PoC加载与执行
"""


class PocLauncher:
    def __init__(self):
        self.operator = {
            'beebeeto': Beebeeto,
            'pocsuite': PocSuite,
            'tangscan': TangScan,
            'kspoc': KsPoc,
        }
        pass

    def verify(self, target, plugin_type, poc_file):
        target = normalize_url(target)
        result = self.operator.get(plugin_type)().run(target, poc_file)
        print(result)

if __name__ == '__main__':
    pl = PocLauncher()
    pl.verify('http://127.0.0.1/', 'beebeeto', 'discuz_x3_0_xss.py')
    pl.verify('http://127.0.0.1/', 'pocsuite', 'drupal_7_x_sql_inj.py')
    pl.verify('http://127.0.0.1/', 'pocsuite', 'git_config_info_disclosure.py')
    pl.verify('http://127.0.0.1/', 'tangscan', 'flash_crossdomain_xml_csrf.py')
    pl.verify('http://127.0.0.1/', 'kspoc', '_1102_discuz_x3_0_static_image_common_focus_swf_xss.py')
