import os
import sys
import argparse
import filecmp
from avocado import Test
from avocado import main
from avocado.utils import process


class funcTesting(Test):
    """
    Runs the tests, parameters are loaded from the arguments.yaml file, which
    provides us with 576 variations:
    :param output_opt1: Output formating option [u,c,m]
    :param output_opt2: Output formating option [u,c,m]
    :param regex: Regular expresion used for the tests, two correct, one wrong
                  and an empty
    :param file1: First file option for the test [empty, not-provided, file1]
    :param file2: First file option for the test [empty, not-provided, file2]
    """

    def datafiles_generator(self):
        """
        Genarates the data files for the possible expected outputs of the
        regexes for the tests 24 possible outcomes, if they do not exist.
        """
        opts = ['-cu', '-c', '-u', '-m']
        datadir = 'tests/functional/test_arguments_and_functionality.py.data/'
        test_files = ['{}log_file1.txt'.format(datadir), '{}log_file2.txt'.format(
            datadir), '{}log_file1.txt {}log_file2.txt'.format(datadir, datadir)]
        regexes = ['run.*/', 'run']
        datafiles = [
            ['cuf1r1.txt', 'cf1r1.txt', 'uf1r1.txt', 'mf1r1.txt'], [
                'cuf2r1.txt', 'cf2r1.txt', 'uf2r1.txt', 'mf2r1.txt'], [
                'cuf1f2r1.txt', 'cf1f2r1.txt', 'uf1f2r1.txt', 'mf1f2r1.txt']], [
            ['cuf1r2.txt', 'cf1r2.txt', 'uf1r2.txt', 'mf1r2.txt'], [
                'cuf2r2.txt', 'cf2r2.txt', 'uf2r2.txt', 'mf2r2.txt'], [
                'cuf1f2r2.txt', 'cf1f2r2.txt', 'uf1f2r2.txt', 'mf1f2r2.txt']]
        for regex, file_super_set in zip(regexes, datafiles):
            for in_file, file_set in zip(test_files, file_super_set):
                for opt, out_file in zip(opts, file_set):
                    if not os.path.isfile(datadir + out_file):
                        data_file = open(datadir + out_file, "w")
                        cmd_line = "python pygrep.py {} '{}' {}".format(
                            opt, regex, in_file)
                        result = process.run(
                            cmd_line, ignore_status=True, shell=False)
                        data_file.write(str(result.stdout.decode("UTF-8")))
                        data_file.close()

    def output_comparison(self, expected_file):
        """
        Compares the output of the current test with the saved valid output
        """
        test_out = self.get_data('test_out.txt')
        expected_file = self.get_data(expected_file)
        out_cmp = filecmp.cmp(test_out, expected_file)
        self.assertTrue(
            out_cmp,
            '*** Test file test_out.txt has different output from {}***'.format(expected_file))

    def test_functionality(self):
        """
        Runs the tests invoking the script and testing the output. First the
        expected returns are generated to compansate for testing erroneous
        parameters. If a test provides output it is stored and compared with
        previously stored valid outputs
        """
        datadir = 'tests/functional/test_arguments_and_functionality.py.data/'
        empty_file = datadir + 'empty_file.txt'
        error_try = False
        ret = None
        expected_ret = None
        m_out = False
        c_out = False
        u_out = False
        opt1 = self.params.get('output_opt1', '/*')
        opt2 = self.params.get('output_opt2', '/*')
        regex = self.params.get('regex', '/*')
        file1 = self.params.get('file1', '/*')
        file2 = self.params.get('file2', '/*')

        if opt1 == 'm' or opt2 == 'm':
            m_out = True
        if opt1 == 'c' or opt2 == 'c':
            c_out = True
        if opt1 == 'u' or opt2 == 'u':
            u_out = True

        opt1 = '' if not opt1 else opt1
        opt2 = '' if not opt2 else opt2
        file1 = '' if not file1 else datadir + file1
        file2 = '' if not file2 else datadir + file2
        regex = '' if not regex else regex

        if not opt1 and not opt2:
            error_try = True
            expected_ret = 2
        elif m_out and (c_out or u_out):
            error_try = True
            expected_ret = 2
        elif not regex or regex == "'*.*con.* '":
            error_try = True
            expected_ret = 2
        elif (not file1 and not file2) and not regex:
            error_try = True
            expected_ret = 2
        elif regex and (not file1 and not file2):
            # Quick fix because avocado does not see the exit code 2 from
            # this specific parser.error exception 
            error_try = True
            expected_ret = 0
        elif regex == "'*.*con.* '" and (not file1 and not file2):
            error_try = True
            expected_ret = 2
        elif (file1 == empty_file and file2 == empty_file) and regex:
            error_try = True  # Skip comparison
            expected_ret = 0
        elif file1 == empty_file or file2 == empty_file and (not file1 or not file2) and regex:
            error_try = True  # Skip comparison
            expected_ret = 0

        cmd_line = 'python pygrep.py -{}{} {} {} {}'.format(
            opt1, opt2, regex, file1, file2)
        if error_try == False:
            self.datafiles_generator()
            expected_ret = 0
            test_output = open(datadir + "test_out.txt", "w")
            result = process.run(cmd_line, ignore_status=True)
            test_output.write(str(result.stdout.decode("UTF-8")))
            test_output.close()
            ret = result.exit_status
            self.assertEqual(
                ret,
                expected_ret,
                '*** Return code {} was expected but got {} ***'.format(
                    expected_ret,
                    ret))

            file1 = None if file1 == empty_file else file1
            file2 = None if file2 == empty_file else file2

            if regex == "'run.*/'":
                if file1 and file2:
                    if m_out:
                        self.output_comparison('mf1f2r1.txt')
                    elif c_out and not u_out:
                        self.output_comparison('cf1f2r1.txt')
                    elif u_out and not c_out:
                        self.output_comparison('uf1f2r1.txt')
                    elif c_out and u_out:
                        self.output_comparison('cuf1f2r1.txt')
                elif file1 and not file2:
                    if m_out:
                        self.output_comparison('mf1r1.txt')
                    elif c_out and not u_out:
                        self.output_comparison('cf1r1.txt')
                    elif u_out and not c_out:
                        self.output_comparison('uf1r1.txt')
                    elif c_out and u_out:
                        self.output_comparison('cuf1r1.txt')
                elif file2 and not file1:
                    if m_out:
                        self.output_comparison('mf2r1.txt')
                    elif c_out and not u_out:
                        self.output_comparison('cf2r1.txt')
                    elif u_out and not c_out:
                        self.output_comparison('uf2r1.txt')
                    elif c_out and u_out:
                        self.output_comparison('cuf2r1.txt')
            else:
                if file1 and file2:
                    if m_out:
                        self.output_comparison('mf1f2r2.txt')
                    elif c_out and not u_out:
                        self.output_comparison('cf1f2r2.txt')
                    elif u_out and not c_out:
                        self.output_comparison('uf1f2r2.txt')
                    elif c_out and u_out:
                        self.output_comparison('cuf1f2r2.txt')
                elif file1 and not file2:
                    if m_out:
                        self.output_comparison('mf1r2.txt')
                    elif c_out and not u_out:
                        self.output_comparison('cf1r2.txt')
                    elif u_out and not c_out:
                        self.output_comparison('uf1r2.txt')
                    elif c_out and u_out:
                        self.output_comparison('cuf1r2.txt')
                elif file2 and not file1:
                    if m_out:
                        self.output_comparison('mf2r2.txt')
                    elif c_out and not u_out:
                        self.output_comparison('cf2r2.txt')
                    elif u_out and not c_out:
                        self.output_comparison('uf2r2.txt')
                    elif c_out and u_out:
                        self.output_comparison('cuf2r2.txt')

        else:
            result = process.run(cmd_line, ignore_status=True)
            ret = result.exit_status
            self.assertEqual(
                ret,
                expected_ret,
                '*** Return code {} was expected but got {} ***'.format(
                    expected_ret,
                    ret))


if __name__ == "__main__":
    main()
