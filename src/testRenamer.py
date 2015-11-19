#!/usr/bin/env python3.4

#import sys, os
#sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

import renamer
import unittest
from nose.tools import assert_equal
#from nose.tools import assert_not_equal
#from nose.tools import assert_raises
#from nose.tools import raises


class TestRenamer(unittest.TestCase):
    def test_make_name(self):
        assert_equal(renamer.make_name('a'), 'a')
        assert_equal(renamer.make_name('abcd'), 'abcd')
        assert_equal(renamer.make_name('Abcd'), 'abcd')
        assert_equal(renamer.make_name('foo-bar'), 'foo-bar')
        assert_equal(renamer.make_name('foo bar'), 'foo-bar')

