import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    CHANGES = ''

version = '1.0.1'

install_requires = [
    'Kotti>=1.3.0',
    'Pillow',  # dependency of plone.scale
    'plone.scale',  # needed for image resizing capabilities
    'rfc6266-parser',
    'unidecode',
]

# copied from Kotti, necessary because extras are not supported in
# ``extras_require``.  See https://github.com/pypa/pip/issues/3189
tests_require = [
    'kotti_image',
    'WebTest',
    'mock',
    'Pillow',  # thumbnail filter in depot tween tests
    'py>=1.4.29',
    'pyquery',
    'pytest>=3.0.0',
    'pytest-cov',
    'pytest-pep8!=1.0.3',
    'pytest-travis-fold',
    'pytest-virtualenv',
    'pytest-xdist',
    'tox',
    'zope.testbrowser>=5.0.0',
    ]

# copied from Kotti, necessary because extras are not supported in
# ``extras_require``.  See https://github.com/pypa/pip/issues/3189
development_requires = [
    'check-manifest',
    'pipdeptree',
    'pyramid_debugtoolbar',
]

setup_requires = [
    'setuptools_git>=0.3',
]


setup(
    name='kotti_image',
    version=version,
    description="Image content type for Kotti",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author='Kotti Developers',
    author_email='kotti@googlegroups.com',
    url='https://github.com/Kotti/kotti_image',
    keywords='kotti web cms wcms pylons pyramid sqlalchemy bootstrap',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    dependency_links=[],
    entry_points={},
    extras_require={
        'testing': tests_require,
        'development': development_requires,
    },
)
