# -*- coding: utf-8 -*-

"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""

from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_image')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_image.kotti_configure

        to enable the ``kotti_image`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_image'
    settings['kotti.alembic_dirs'] += ' kotti_image:alembic'
    settings['kotti.available_types'] += ' kotti_image.resources.Image'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_image:locale')
    config.add_static_view('static-kotti_image', 'kotti_image:static')

    config.scan(__name__)
