#!/usr/bin/python3
# Fabfile to delete out-of-date archives.

from fabric.api import *
from os.path import exists
import time

env.hosts = ['34.237.91.138', '34.203.38.155']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """

    # Convert the number parameter to integer
    number = int(number)

    # Build the components of the command
    ls_command = 'ls -t versions'
    tail_command = 'tail -n +2'
    rm_command = 'xargs rm -f --'
    command = 'ls -t /data/web_static/releases'

    # If number is 0 or 1, keep only the most recent version of your archive
    if number == 0 or number == 1:
        local('{} | {} | {}'.format(ls_command, tail_command, rm_command))
        run('{} | {} | {}'.format(command, tail_command, rm_command))
    else:
        # If number is 2 or more, keep the most recent
        local(
            'ls -t versions | tail -n +{} | xargs rm -f --'.format(number + 1)
        )
        run('{} | tail -n +{} | xargs rm -rf --'.format(command, number + 1))
