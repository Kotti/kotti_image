# -*- coding: utf-8 -*-

"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():

    return {
        # 'kotti.configurators': 'kotti_image.kotti_configure'
    }
