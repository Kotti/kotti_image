import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, "README.rst")).read()
except IOError:
    README = ""
try:
    CHANGES = open(os.path.join(here, "CHANGES.rst")).read()
except IOError:
    CHANGES = ""

version = "2.0.0"

install_requires = [
    "Kotti>=2.0.4",
    "Pillow",
    "plone.scale",
]

tests_require = [
    'WebTest',
    'mock',
    'Pillow',  # thumbnail filter in depot tween tests
    'pyquery',
    'pytest<5',
    'pytest-cov',
    'pytest-flake8',
    'pytest-virtualenv',
    'zope.testbrowser>=5.0.0',
]

development_requires = [
    "Kotti[development]",
    "pyramid_debugtoolbar",
]

setup_requires = [
    "setuptools_git>=0.3",
]

setup(
    name="kotti_image",
    version=version,
    description="Image content type for Kotti",
    long_description="\n\n".join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author="Kotti Developers",
    author_email="kotti@googlegroups.com",
    url="https://github.com/Kotti/kotti_image",
    keywords="kotti web cms wcms pylons pyramid sqlalchemy bootstrap",
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
        "testing": tests_require,
        "development": development_requires,
    },
)
