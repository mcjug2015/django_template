'''
    module for file based shell command runner.
    avoid exposing to the outside world.
'''
# pylint: disable=R0914,W0702
import shlex
import subprocess
import sys
import traceback
import logging
from django.core.management.base import BaseCommand


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    '''
        This command grabs a file, executes each line in it via
        popen and writes convenient output files for the ones that failed
    '''

    def add_arguments(self, parser):
        parser.add_argument('input_file_path', nargs=1)
        parser.add_argument('error_file_path', nargs=1)
        parser.add_argument('error_detail_file_path', nargs=1)

    def handle(self, *args, **options):
        '''
            opens file, reads each line, executes, keeps track of the ones that
            fail somehow.
        '''
        command_handle = open(options['input_file_path'][0])
        error_handle = open(options['error_file_path'][0], 'w')
        error_detail_handle = open(options['error_detail_file_path'][0], 'w')
        LOGGER.info("Gonna run commands from %s, list errors in %s, list detail errors in %s",
                    options['input_file_path'][0],
                    options['error_file_path'][0],
                    options['error_detail_file_path'][0])

        commands_found = 0
        commands_succeeded = 0
        for single_command in command_handle:
            stripped_command = single_command.strip()
            if stripped_command:
                commands_found += 1
                try:
                    command_args = shlex.split(stripped_command)
                    LOGGER.info("Found command %s,\nsplit into %s,\nabout to execute",
                                stripped_command, command_args)
                    proc = subprocess.Popen(command_args,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                    output, err_output = proc.communicate()
                    if proc.returncode != 0:
                        LOGGER.info("Prev command failed, err output was %s",
                                    err_output)
                        error_handle.write(stripped_command + '\n')
                        error_detail_handle.write('%s\n%s\n%s\n\n' % (stripped_command,
                                                                      output,
                                                                      err_output))
                    else:
                        commands_succeeded += 1
                except:
                    LOGGER.info("Prev command failed with os error")
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    error_handle.write(stripped_command + '\n')
                    error_detail_handle.write('%s\n%s\n\n' % (stripped_command,
                                                              ''.join(lines)))
        command_handle.close()
        error_handle.close()
        error_detail_handle.close()
        commands_failed = commands_found - commands_succeeded
        LOGGER.info("Ran %s commands, of them %s succeeded and %s failed",
                    commands_found, commands_succeeded, commands_failed)
