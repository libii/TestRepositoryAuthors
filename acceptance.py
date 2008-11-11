#!/usr/bin/env python
"""
This is an acceptance test for the meshPartition 
"""

import unittest
import os
import sys
import filecmp

class accept_test(unittest.TestCase):

    def setUp(self):
        print ""

    def tearDown(self):
        print ""

    def test1(self):
       print ""
       print "Starting meshPartition acceptance test"
       print ""
       a_ref_dir = "./reference_values"
       a_tmp_dir = "./tests"

       a_ref_file = a_ref_dir + "/mesh_0_0_0.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_0_0_0.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""
       a_ref_file = a_ref_dir + "/mesh_0_0_1.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_0_0_1.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""

       a_ref_file = a_ref_dir + "/mesh_0_1_0.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_0_1_0.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""
       a_ref_file = a_ref_dir + "/mesh_0_1_1.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_0_1_1.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""
       a_ref_file = a_ref_dir + "/mesh_1_0_0.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_1_0_0.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""
       a_ref_file = a_ref_dir + "/mesh_1_0_1.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_1_0_1.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""
       a_ref_file = a_ref_dir + "/mesh_1_1_0.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_1_1_0.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""
       a_ref_file = a_ref_dir + "/mesh_1_1_1.bin"
       print "a_ref_file: %s"%(a_ref_file)
       a_tmp_file = a_tmp_dir + "/mesh_1_1_1.bin"
       print "a_tmp_file: %s"%(a_tmp_file)
       self.assertTrue(filecmp.cmp(a_tmp_file,a_ref_file))

       print ""

       print ""
       print "completed meshPartition acceptance test"
       print ""

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(accept_test)
    unittest.TextTestRunner(verbosity=2).run(suite)

