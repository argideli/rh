import os
#import glob
import subprocess
#import logging
#import time
import sys
import argparse
try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2
from avocado import Test
from avocado import main
#from avocado import mock

sys.path.append('../..')
sys.path.append('./')
import pygrep

class ArgumentTesting(Test):

    #os.chdir('../../')

    def test_random_arg(self):
        opt1 = self.params.get('output_opt1', '/*')
        opt2 = self.params.get('output_opt2', '/*')
        regex = self.params.get('regex', '/*')
        file1 = self.params.get('file1', '/*')
        file2 = self.params.get('file2', '/*')
        print('PARAMS=============',opt1, opt2, regex, file1, file2)
        print(type(regex))
        #with mock.patch('pygrep.regSearch.argument_handler', return_value=argparse.Namespace(underscore=True,color=True, machine=False, regex=['jedi'], files=[open('../../docs/test_files/file2.txt', 'r')])):
        #    finder = pygrep.regSearch()
        #    for file in finder.args.files:
        #        print("TESTTTTTTTTTTTTTTTTTTTTTTT:",file)
        #        finder.run(file)
        #        file.close()
            #finder.run('../../docs/test_files/file1.txt')
            #print('RESSSSSSSSSS=========='+finder.args)
        #data = TestData.get_data(filename='file2.txt')
        #exit(2)
        #cmd_line = 'python pygrep.py some-random-text'
        #ret = subprocess.call(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #expected_ret = 2
        #self.assertEqual(ret, expected_ret,
        #                 'pygrep did not return : %d:\n%s' % (expected_ret, ret))

if __name__ == "__main__":
    main()
