# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import codecs
import os.path
import re
from setuptools import setup, find_packages, Command


# metadata

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'loafer/__init__.py'), encoding='utf-8') as f:
    # this adds __version__ to setup.py
    exec(f.read())


version = "0.0.0"
changes = os.path.join(here, "CHANGES.rst")
pattern = r'^(?P<version>[0-9]+.[0-9]+(.[0-9]+)?)'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        match = re.match(pattern, line)
        if match:
            version = match.group("version")
            break


class VersionCommand(Command):
    description = 'Show library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)  # NOQA


with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n{}'.format(f.read())

with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changes = f.read()
    long_description += '\n\nChangelog:\n----------\n\n{}'.format(changes)


# Requirements

# Unduplicated tests_requirements and requirements/test.txt
tests_requirements = ['pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-env',
                      'coveralls', 'asynctest']

install_requirements = ['boto3>=1.3.0',
                        'cached-property>=1.3.0',
                        ]


# setup

setup(
    name="olist-loafer",
    version=version,  # NOQA
    description='Asynchronous message dispatcher for concurrent tasks processing',
    long_description=long_description,
    url='https://github.com/solidarium/loafer/',
    download_url='https://github.com/solidarium/loafer/releases',
    license='MIT',
    author='George Y. Kussumoto and Olist Developers',
    author_email='contato at georgeyk dot com dot br and developers@olist.com',
    packages=find_packages(exclude=['docs', 'tests', 'tests.*', 'requirements']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Distributed Computing',
        ],
    keywords='asynchronous asyncio message dispatcher tasks',
    setup_requires=['pytest-runner'],
    install_requires=install_requirements,
    tests_require=tests_requirements,
    cmdclass={
        'version': VersionCommand
    },
)
