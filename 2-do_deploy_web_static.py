#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""


from fabric.api import *
import os

env.hosts = ['100.26.167.18', '54.175.189.193']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.

    This function uploads the given archive to your web servers, uncompresses
    it, creates a symbolic link, and cleans up old releases.

    Args:
        archive_path (str): The path to the archive on your local machine.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]

        # Upload the archive to the /tmp/ directory of the web servers
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))

        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_name, archive_no_ext))

        # Delete the archive from the web servers
        run('rm /tmp/{}'.format(archive_name))

        # Delete the old symbolic link
        run('rm -f /data/web_static/current')

        # Create a new symbolic link to the new release
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_no_ext))

        return True
    except Exception:
        return False
