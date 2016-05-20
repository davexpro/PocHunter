#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160518

import imp
import sys

from config import PLUGINS_DIR, POCS_DIR


class PocSuite:
    def __init__(self):
        self.plugins_name = 'pocsuite'
        self.result = {
            'vul_info': {},
            'result': {}
        }

    def import_poc(self, path):
        try:
            sys.path.append(PLUGINS_DIR)
            path = POCS_DIR + self.plugins_name + '/' + path
            poc = imp.load_source('TestPOC', path)
            poc = poc.TestPOC()
            return poc
        except Exception as e:
            print('[-] Frame.Pocsuite Import PoC Error: {0}'.format(str(e)))
            return None

    @staticmethod
    def get_vul_info(poc):
        vul_info = {
            'name': poc.name,
            'desc': poc.desc,
        }
        return vul_info

    def run(self, target, path):
        try:
            poc = self.import_poc(path)
            if poc is None:
                return
            verify_result = poc.execute(target, mode='verify')
            if verify_result.result:
                self.result['vul_info'] = self.get_vul_info(poc)
                self.result['result'] = verify_result.result
                return self.result
            else:
                return False
        except Exception as e:
            print('[-] Frame.Pocsuite Detail: {0}'.format(str(e)))
            return
