#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import uuid
from random import choice


def username(prefix='BB2test'):
    return prefix + str(hash(str(uuid.uuid4())) % 10000000)


def password(length=10, chars=string.letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])
