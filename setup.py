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

version = '1.0.0.dev0'

install_requires = [
    'Kotti>=1.3.0<2.0.0.dev0',
    'Pillow',  # dependency of plone.scale
    'plone.scale',  # needed for image resizing capabilities
    'rfc6266-parser',
    'unidecode',
]

tests_require = [
    'Kotti>=1.3.0[testing]'
]

development_requires = [
    'check-manifest',
    'pipdeptree',
    'pyramid_debugtoolbar',
]


setup(
    name='kotti_image',
    version=version,
    description="Image content type for Kotti",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author='Kotti developers',
    author_email='kotti@googlegroups.com',
    url='https://github.com/Kotti/kotti_image',
    keywords='kotti web cms wcms pylons pyramid sqlalchemy bootstrap',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    dependency_links=[],
    entry_points={},
    extras_require={
        'testing': tests_require,
        'development': development_requires,
    },
)
