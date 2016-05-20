#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160518
import imp
import sys

from config import PLUGINS_DIR, POCS_DIR


class TangScan:
    def __init__(self):
        self.plugins_name = 'tangscan'
        self.result = {
            'vul_info': {},
            'result': {}
        }

    def import_poc(self, path):
        sys.path.append(PLUGINS_DIR + self.plugins_name + '/tangscan')
        path = POCS_DIR + self.plugins_name + '/' + path
        poc = imp.load_source('TangScan', path)
        poc = poc.TangScan()
        return poc

    @staticmethod
    def get_vul_info(poc):
        vul_info = {
            'name': poc.info['name'],
            'desc': poc.result['description'],
        }
        return vul_info

    def run(self, target, path):
        try:
            poc = self.import_poc(path)
            poc.option.url = target
            poc.verify()
            if poc.result.status:
                self.result['vul_info'] = self.get_vul_info(poc)
                self.result['result'] = poc.result.data
                return self.result
            else:
                return False
        except Exception as e:
            print('[-] Frame.TangScan Detail: {0}'.format(str(e)))
            return
