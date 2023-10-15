#!/usr/bin/env python3
# coding=utf-8

import sys

if sys.version_info < (3, 5):
    print("This application requires at least Python 3.5")
    quit(1)

from nyankocoin.core.misc.DependencyChecker import DependencyChecker

DependencyChecker.check()

from nyankocoin.main import main

main()
