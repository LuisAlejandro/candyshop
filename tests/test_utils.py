#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------

Tests for `utils` module.
"""


import doctest

def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('candyshop.utils'))
    return tests

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
