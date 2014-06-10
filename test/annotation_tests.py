#!/usr/bin/env python

import unittest
import io
from src.ipr import read_ipr

class TestAnnotation(unittest.TestCase):


    def test_write_annotations(self): #this function is pretty trivial
       pass


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAnnotation))
    return suite

if __name__ == '__main__':
    unittest.main()
