#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import ast
import re
import types

from pocsuite.thirdparty.requests.exceptions import ConnectTimeout


class POCBase(object):
    def __init__(self):
        self.type = None
        self.target = None
        self.url = None
        self.mode = None
        self.params = None
        self.verbose = None

    def execute(self, target, headers=None, params=None, mode='verify', verbose=True):
        """
        :param url: the target url
        :param headers: a :class dict include some fields for request header.
        :param params: a instance of Params, includ extra params

        :return: A instance of Output
        """
        self.target = target
        self.url = parseTargetUrl(target)
        self.headers = headers
        self.params = strToDict(params) if params else {}
        self.mode = mode
        self.verbose = verbose
        # TODO
        output = None

        try:
            if self.mode == 'attack':
                output = self._attack()
            else:
                output = self._verify()

        except NotImplementedError:
            output = Output(self)

        except ConnectTimeout, e:
            retry = 5
            while retry > 0:
                try:
                    if self.mode == 'attack':
                        output = self._attack()
                    else:
                        output = self._verify()
                    break
                except ConnectTimeout:
                    output = Output(self)
                retry -= 1
            else:
                output = Output(self)

        except Exception, e:
            output = Output(self)

        return output

    def _attack(self):
        '''
        @function   以Poc的attack模式对urls进行检测(可能具有危险性)
                    需要在用户自定义的Poc中进行重写
                    返回一个Output类实例
        '''
        raise NotImplementedError

    def _verify(self):
        '''
        @function   以Poc的verify模式对urls进行检测(可能具有危险性)
                    需要在用户自定义的Poc中进行重写
                    返回一个Output类实例
        '''
        raise NotImplementedError

    """
    def _kwargsPatch(self, func):
        def wrapper(*args, **kwargs):

            try:
                userHeaders = kwargs['headers']
            except:
                userHeaders = {}

            kwargs.update({'headers': self.headers})
            kwargs['headers'].update(userHeaders)
            return func(*args, **kwargs)
        return wrapper

    req.get = _kwargsPatch(req.get)
    """


class Output(object):
    ''' output of pocs
    Usage::
        >>> poc = POCBase()
        >>> output = Output(poc)
        >>> result = {'FileInfo': ''}
        >>> output.success(result)
        >>> output.fail('Some reason failed or errors')
    '''

    def __init__(self, poc=None):
        if poc:
            self.url = poc.url
            self.mode = poc.mode
            self.vulID = poc.vulID
            self.name = poc.name
            self.appName = poc.appName
            self.appVersion = poc.appVersion
        self.error = ""
        self.result = {}
        self.status = 0

    def is_success(self):
        return bool(True and self.status)

    def success(self, result):
        assert isinstance(result, types.DictType)
        self.status = 1
        self.result = result

    def fail(self, error):
        self.status = 0
        assert isinstance(error, types.StringType)
        self.error = error

    def show_result(self):
        pass


def parseTargetUrl(url):
    """
    Parse target URL
    """
    retVal = url

    if not re.search("^http[s]*://", retVal, re.I) and not re.search("^ws[s]*://", retVal, re.I):
        if re.search(":443[/]*$", retVal):
            retVal = "https://" + retVal
        else:
            retVal = "http://" + retVal

    return retVal


def strToDict(string):
    try:
        return ast.literal_eval(string)
    except ValueError as e:
        pass
