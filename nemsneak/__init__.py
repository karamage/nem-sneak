# -*- coding: utf-8 -*-

__description__ = u'nemsneak'

__long_description__ = u'''nemsneak
'''

__author__ = u'osoken'
__email__ = u'osoken.devel@outlook.jp'
__version__ = '0.0.0'

__package_name__ = u'nemsneak'

try:
    from . import core
    Connection = core.Connection
    Gazer = core.Gazer
except Exception as e:
    x = e

    def _(*args, **kwargs):
        raise x

    Connection = _
    Gazer = _
