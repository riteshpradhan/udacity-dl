#!/usr/bin/env python

from setuptools import setup

setup(name="udacity-dl",
            version="1.0",
            description="Download udacity class videos and resources",
            long_description=open("README.md").read(),
            author="Ritesh Pradhan",
            author_email="ritesxz@gmail.com",
            url="https://github.com/ritespradhan/udacity-dl",
            packages=["udacity-dl"],
            entry_points = { "console_scripts" : [ "udacity-dl = udacity-dl.udacity-dl:main"]},
            install_requires=["mechanize","beautifulsoup4","argparse"],
           )
