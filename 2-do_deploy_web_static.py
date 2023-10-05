#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""


from fabric.api import env, put, run, sudo
import os

env.hosts = ['100.26.167.18', '54.175.189.193']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    This function uploads the specified archive to the web servers,
    extracts it to the appropriate directory, creates a symbolic link
    to the new version, and performs cleanup.

    Args:
        archive_path (str): The path to the archive file on the local machine.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the web servers
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        archive_filename = os.path.basename(archive_path)
        release_dir = "/data/web_static/releases/{}".format(
            archive_filename.split('.')[0]
        )
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_dir))

        # Delete the uploaded archive from /tmp/
        run("rm /tmp/{}".format(archive_filename))

        # Remove the current symbolic link if it exists
        current_link = "/data/web_static/current"
        if run("test -L {}".format(current_link)).succeeded:
            run("rm {}".format(current_link))

        # Create a new symbolic link to the new version
        run("ln -s {} {}".format(release_dir, current_link))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", str(e))
        return False
