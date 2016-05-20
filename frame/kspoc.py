#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20160518

import imp
import sys

from config import PLUGINS_DIR, POCS_DIR


class KsPoc:
    def __init__(self):
        self.io_info = {
            'Status': 0,
            'Verbose': False,
            'Mode': 'v',
            'Error': '',
            'Result': {}
        }
        self.plugins_name = 'kspoc'
        self.result = {
            'vul_info': {},
            'result': {}
        }

    def import_poc(self, path):
        sys.path.append(PLUGINS_DIR + self.plugins_name)
        path = POCS_DIR + self.plugins_name + '/' + path
        poc = imp.load_source('main', path)
        return poc

    @staticmethod
    def get_vul_info(poc):
        vul_info = {
            'name': poc.poc_info['Name'],
            'desc': poc.poc_info['Desc'],
        }
        return vul_info

    def run(self, target, path):
        try:
            poc = self.import_poc(path)
            self.io_info['URL'] = target
            poc.main(self.io_info)
            if self.io_info['Status'] == 1:
                self.result['vul_info'] = self.get_vul_info(poc)
                self.result['result'] = self.io_info['Result']
                return self.result
            else:
                return False
        except Exception as e:
            print('[-] Frame.KSPoC Detail: {0}'.format(str(e)))
            return
