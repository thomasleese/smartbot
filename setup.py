#!/usr/bin/env python3
import ez_setup
ez_setup.use_setuptools()

from setuptools import find_packages, setup


setup(
    name='smartbot',
    version='1.0.0',
    description='A supposedly smart IRC bot.',
    url='https://github.com/tomleese/smartbot',
    author='Tom Leese',
    author_email='inbox@tomleese.me.uk',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'PyYaml',
        'lxml',
        'requests == 2.1.0',
        'isodate',
        'textblob',
        'twython',
        'cssselect',
        'python-dateutil'
    ],
    entry_points={
        'console_scripts': ['smartbot = smartbot.cli:main']
    },
    test_suite='tests'
)
