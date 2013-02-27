#!/usr/bin/env python

from setuptools import setup

setup(name="udacity-dl",
            version="1.1.1",
            description="Download udacity class videos and resources",
            long_description=open("README.md").read(),
            author="Ritesh Pradhan",
            author_email="ritesxz@gmail.com",
            url="https://github.com/ritespradhan/udacity-dl",
            packages=["udacitydl"],
            entry_points = { "console_scripts" : [ "udacity-dl = udacitydl.udacitydl:main"]},
            install_requires=["mechanize","beautifulsoup4","argparse"],
           )
