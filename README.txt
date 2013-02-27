udacity-dl
===========

A python package for archiving content from udacity.org (videos,
lecture notes, quizzes, …) for offline reference.

Installation
------------

Make sure you have installed [Python][] 2.7

Then simply run: python setup.py install

This will create a udacity-dl script in /usr/local/bin (linux) or
c:\\Pytohon2.7\\Scripts (windows)


Usage 
------

See: udacity-dl -h

Example usage:

udacity-dl  -d /my/destination/path/ course_name(s)  

  [Python]: http://www.python.org/download/


Notes
-----

For the link:
https://www.udacity.com/wiki/ST095/downloads

"ST095"  is the course_name

Usage:
udacity-dl  -d /my/destination/path/ ST095 cs222


Features
--------

* Now downloads all available resources in wiki
* Skips already downloaded resources
* Proper naming of course and class contents
* No need of Udacity username and password

=======
==========
