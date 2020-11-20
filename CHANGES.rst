History
=======

- Drop support for Python 2.
- Remove dependency from ``rfc_6266_parser`` and use
  ``depot.utils.make_content_disposition`` instead.

1.0.1 - 2018-03-16
------------------

- Use ``rfc_6266_parser`` instead of unmaintained ``rfc_6266`` package.
- Fix tests for Kotti >= 2.0.0 / Python 3.x.

1.0.0 - 2018-01-17
------------------

- No functional changes.  Maintainance release for Kotti 1.x.
- Integrate filedepot tween / filter test from Kotti < 2.0.0.

0.1.4 - 2016-10-09
------------------

- Correctly declare dependencies.

0.1.3 - 2016-01-04
------------------

- Include (empty) ``alembic/versions`` directory in distribution to avoid
  warnings.

0.1.2 - 2015-12-21
------------------

- Use rfc6266 and unidecode for content disposition header.

0.1.1 - 2015-12-16
------------------

- Fix broken packaging.

0.1.0 - 2015-12-16
------------------

This initial version is completely identical to what has been in Kotti core
before Kotti 1.3.0-dev.  **Don't even try to install with those versions!**

- Move all image related code from Kotti core into this package.
- Create package with ``pcreate -s kotti kotti_image``.
