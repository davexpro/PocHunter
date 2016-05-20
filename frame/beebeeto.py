#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160518

import imp
import sys

from config import POCS_DIR, PLUGINS_DIR


class Beebeeto:
    def __init__(self):
        self.plugins_name = 'beebeeto'
        self.result = {
            'vul_info': {},
            'result': {}
        }

    def import_poc(self, path):
        sys.path.append(PLUGINS_DIR + self.plugins_name)
        path = POCS_DIR + self.plugins_name + '/' + path
        poc = imp.load_source('MyPoc', path)
        return poc

    @staticmethod
    def get_vul_info(poc):
        vul_info = {
            'name': poc.MyPoc.poc_info['poc']['name'],
            'desc': poc.MyPoc.poc_info['vul']['desc'],
        }
        return vul_info

    def run(self, target, path):
        try:
            poc = self.import_poc(path)
            options = {
                'target': target,
                'verify': True,
                'verbose': False,
            }
            ret = poc.MyPoc(False).run(options=options, debug=False)
            if ret['success']:
                self.result['vul_info'] = self.get_vul_info(poc)
                self.result['result'] = ret['poc_ret']
                return self.result
            else:
                return False
        except Exception as e:
            print('[-] Frame.Beebeeto Detail: {0}'.format(str(e)))
            return
