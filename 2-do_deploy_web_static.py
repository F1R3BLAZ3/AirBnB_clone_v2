#!/usr/bin/python3
"""
Fabric script that distributes an archive to your
web servers, using the function do_deploy
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['34.237.91.138', '34.203.38.155']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        filetype = filename.split(".")[0]
        directory = "/data/web_static/releases/{}/".format(filetype)

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(directory))
        run('tar -xzf /tmp/{} -C {}'.format(filename, directory))
        run('rm /tmp/{}'.format(filename))
        run('mv {}web_static/* {}'.format(directory, directory))
        run('rm -rf {}web_static'.format(directory))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(directory))
        return True
    except Exception as e:
        print("Error:", str(e))
        return False
