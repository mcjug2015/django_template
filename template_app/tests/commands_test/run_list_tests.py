''' test module for the run list command '''
import os
import shutil
from tempfile import mkdtemp
from mockito.mockito import unstub, when, verify, mock
from django.test.testcases import TestCase
from template_app.management.commands import run_list


class RunListTests(TestCase):
    ''' test class for the run list command '''

    def setUp(self):
        ''' set up the test '''
        self.run_list = run_list.Command()
        self.work_dir = mkdtemp()
        self.res_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'commands_test')
        self.err_report_path = os.path.join(self.work_dir, 'err_report.txt')
        self.err_detail_report_path = os.path.join(self.work_dir, 'err_detail_report.txt')
        self.options = {'error_file_path': [self.err_report_path],
                        'error_detail_file_path': [self.err_detail_report_path]}

    def tearDown(self):
        ''' tear down the test '''
        unstub()
        shutil.rmtree(self.work_dir)

    def test_good_command(self):
        '''
            make sure nothing shows up in the error report files when commands are good
            and successful
        '''
        self.options['input_file_path'] = [os.path.join(self.res_path, 'good_command.txt')]
        self.run_list.handle(input_file_path=self.options['input_file_path'],
                             error_file_path=self.options['error_file_path'],
                             error_detail_file_path=self.options['error_detail_file_path'])
        self.assertFalse(open(self.err_report_path).read().strip())
        self.assertFalse(open(self.err_detail_report_path).read().strip())

    def test_failing_command(self):
        '''
            make sure we see a failing command listed in error reports
        '''
        self.options['input_file_path'] = [os.path.join(self.res_path, 'bad_failing_command.txt')]
        self.run_list.handle(input_file_path=self.options['input_file_path'],
                             error_file_path=self.options['error_file_path'],
                             error_detail_file_path=self.options['error_detail_file_path'])
        err_output = open(self.err_report_path).read().strip()
        err_detail_output = open(self.err_detail_report_path).read().strip()
        self.assertGreater(len(err_output), 0)
        self.assertGreater(len(err_detail_output), 0)
        self.assertEquals('/usr/bin/ls -i_will_fail', err_output)
        self.assertIn('/usr/bin/ls -i_will_fail', err_detail_output)
        self.assertIn('invalid option', err_detail_output)

    def test_exploding_command(self):
        '''
            make sure an exploding command puts info into error reports
        '''
        self.options['input_file_path'] = [os.path.join(self.res_path, 'bad_exploding_command.txt')]
        self.run_list.handle(input_file_path=self.options['input_file_path'],
                             error_file_path=self.options['error_file_path'],
                             error_detail_file_path=self.options['error_detail_file_path'])
        err_output = open(self.err_report_path).read().strip()
        err_detail_output = open(self.err_detail_report_path).read().strip()
        self.assertGreater(len(err_output), 0)
        self.assertGreater(len(err_detail_output), 0)
        self.assertEquals('i_will_fail', err_output)
        self.assertIn('i_will_fail', err_detail_output)
        self.assertIn('OSError', err_detail_output)

    def test_add_arguments(self):
        ''' verify that expected arguements are added to the parser '''
        the_parser = mock()
        when(the_parser).add_argument('input_file_path', nargs=1).thenReturn(None)
        when(the_parser).add_argument('error_file_path', nargs=1).thenReturn(None)
        when(the_parser).add_argument('error_detail_file_path', nargs=1).thenReturn(None)
        self.run_list.add_arguments(the_parser)
        verify(the_parser).add_argument('input_file_path', nargs=1)
        verify(the_parser).add_argument('error_file_path', nargs=1)
        verify(the_parser).add_argument('error_detail_file_path', nargs=1)
