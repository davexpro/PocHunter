#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160520
from lib.poc_launcher import PocLauncher
"""
* Author Dave
* Version 1.0
* 测试用例
"""

if __name__ == '__main__':
    pl = PocLauncher()
    pl.verify('http://127.0.0.1/', 'beebeeto', 'discuz_x3_0_xss.py')
    pl.verify('http://127.0.0.1/', 'pocsuite', 'drupal_7_x_sql_inj.py')
    pl.verify('http://127.0.0.1/', 'pocsuite', 'git_config_info_disclosure.py')
    pl.verify('http://127.0.0.1/', 'tangscan', 'flash_crossdomain_xml_csrf.py')
    pl.verify('http://127.0.0.1/', 'kspoc', '_1102_discuz_x3_0_static_image_common_focus_swf_xss.py')
