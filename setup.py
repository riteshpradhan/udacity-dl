#!/usr/bin/env python

from setuptools import setup

setup(name="udacity-dl",
      version="2.0.0",
      description="Download udacity class videos and resources",
      long_description=open("README").read(),
      author="Ritesh Pradhan",
      author_email="ritesxz@gmail.com",
      url="https://github.com/riteshpradhan/udacity-dl",
      download_url="https://pypi.python.org/pypi/udacity-dl",
      packages=["udacitydl"],
      entry_points = { "console_scripts" : [ "udacity-dl = udacitydl.udacitydl:main"]},
      install_requires=["mechanicalsoup","tqmd"],
     )
