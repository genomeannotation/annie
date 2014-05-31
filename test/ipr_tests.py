#!/usr/bin/env python

import unittest
import io
from src.ipr import read_ipr

class TestIPR(unittest.TestCase):

    def setUp(self):
        self.ipr_file = io.StringIO(\
        'm.98281\tc95b0824ccd627403aa63f9e474649cc\t7571\tSUPERFAMILY\tSSF48726\t5997\t6096\t6.42E-13\tT\t04-04-2014\nm.98281\tc95b0824ccd627403aa63f9e474649cc\t7571\tProSiteProfiles\tPS50835\tIg-like domain profile.\t6294\t6382\t12.15\tT\t04-04-2014IPR007110\tImmunoglobulin-like domain\tGO:0005515\nm.98281\tc95b0824ccd627403aa63f9e474649cc\t7571\tProSiteProfiles\tPS50835\tFibronectin type-III domain profile.\t2548\t2639\t21.089\tT\t04-04-2014\tIPR003961\tFibronectin, type III\tGO:0005515\n')

    def test_read_ipr(self):
        whitelist = ["superfamily", "prositeprofiles"]
        ipr_list = read_ipr(self.ipr_file, whitelist)
        self.assertEquals(2, len(ipr_list))
        first_entry = ipr_list[0]
        second_entry = ipr_list[1]
        mrna_ids = [first_entry[0], second_entry[0]]
        self.assertTrue("m.98281" in mrna_ids)
        self.assertEquals("Dbxref", first_entry[1])
        dbxrefs = [first_entry[2], second_entry[2]]
        self.assertTrue("SUPERFAMILY:SSF48726" in dbxrefs)


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIPR))
    return suite

if __name__ == '__main__':
    unittest.main()
