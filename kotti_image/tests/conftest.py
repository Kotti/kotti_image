"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope="session")
def custom_settings():
    # noinspection PyUnresolvedReferences
    from kotti_image.resources import Image

    return {
        "kotti.configurators": "kotti_image.kotti_configure",
    }


@fixture
def app(db_session, setup_app):
    from webtest import TestApp

    return TestApp(setup_app)
