# -*- coding: utf-8 -*-

"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    # Compatibility for Kotti 1.3 and 2.0
    try:
        from kotti.resources import Image
        return {}
    except ImportError:
        # noinspection PyUnresolvedReferences c
        from kotti_image.resources import Image
        return {
            'kotti.configurators': 'kotti_image.kotti_configure'
        }
