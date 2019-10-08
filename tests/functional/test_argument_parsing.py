import os
import glob
import unittest
import subprocess

#from .. import pygrep


class ArgumentTesting(unittest.TestCase):

    os.chdir('../../')

    def test_random_arg(self):
        cmd_line = 'python pygrep.py some-random-text'
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_no_args(self):
        cmd_line = 'python pygrep.py'
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_few_args1(self):
        cmd_line = "python pygrep.py -c"
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_no_file(self):
        cmd_line = "python pygrep.py -c 'exp'"
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_not_existing_file(self):
        cmd_line = "python pygrep.py -c 'exp' some_file_that_does_not_exist"
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_no_format(self):
        cmd_line = "python pygrep.py 'exp' docs/test_files/file2.txt"
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_multiple_formats1(self):
        cmd_line = "python pygrep.py -cm 'exp' docs/test_files/file2.txt"
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

    def test_multiple_formats2(self):
        cmd_line = "python pygrep.py -cmu 'exp' docs/test_files/file2.txt"
        ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        expected_ret = 2
        self.assertEqual(ret, expected_ret,
                         'pygrep did not return : %d:\n%s' % (expected_ret, ret))

if __name__ == '__main__':
    unittest.main()
