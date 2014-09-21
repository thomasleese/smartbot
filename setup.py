#!/usr/bin/env python3
from setuptools import setup

setup(
    name="smartbot",
    version="1.0.0-dev",
    description="A supposedly smart IRC bot.",
    url="https://github.com/tomleese/smartbot",
    author="Tom Leese",
    author_email="tom@tomleese.me.uk",
    packages=["smartbot", "smartbot.backends", "smartbot.plugins", "smartbot.stores", "smartbot.utils"],
    install_requires=[
        "PyYaml",
        "lxml",
        "requests==2.1.0",
        "isodate",
        "textblob",
        "twython",
        "cssselect"
    ],
    entry_points = {
        "console_scripts": ["smartbot = smartbot:main"]
    }
)
