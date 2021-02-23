import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "smartbms_monitor",
    version = "0.0.1",
    author = "Tom Catling",
    author_email = "tomcatling@gmail.com",
    description = ("Tools for monitoring 123\SmartBMS"),
    license = "BSD",
    keywords = "smartbms 123 bms",
    packages=['smartbms_monitor'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)