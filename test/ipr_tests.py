#!/usr/bin/env python

import unittest
import io
from src.ipr import read_ipr

class TestIPR(unittest.TestCase):

    def setUp(self):
        self.ipr_file = io.StringIO(\
        'm.98281\tc95b0824ccd627403aa63f9e474649cc\t7571\tSuperFamily\tSSF48726\t5997\t6096\t6.42E-13\tT\t04-04-2014\n\
m.98281\tc95b0824ccd627403aa63f9e474649cc\t7571\tProSiteProfiles\tPS50835\tIg-like domain profile.\t6294\t6382\t12.15\tT\t04-04-2014\tIPR007110\tImmunoglobulin-like domain\tGO:0005515\n\
m.98281\tc95b0824ccd627403aa63f9e474649cc\t7571\tProSiteProfiles\tPS50835\tFibronectin type-III domain profile.\t2548\t2639\t21.089\tT\t04-04-2014\tIPR003961\tFibronectin, type III\tGO:0005515\n')

    def test_read_ipr(self):
        whitelist = ["superfamily", "prositeprofiles"]
        ipr_list = read_ipr(self.ipr_file, whitelist)
        self.assertEquals(5, len(ipr_list))
        mrna_ids = [ipr_list[i].feature_id for i in range(len(ipr_list))]
        keys = [ipr_list[i].key for i in range(len(ipr_list))]
        values = [ipr_list[i].value for i in range(len(ipr_list))]
        self.assertTrue("m.98281" in mrna_ids)
        self.assertTrue("Dbxref" in keys)
        self.assertTrue("GO" in keys)
        self.assertTrue("SUPERFAMILY:SSF48726" in values)
        self.assertTrue("GO:0005515" in values)
        self.assertTrue("IPR007110" in values)



##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIPR))
    return suite

if __name__ == '__main__':
    unittest.main()
