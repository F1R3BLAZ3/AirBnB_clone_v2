#!/usr/bin/python3
from fabric.api import local, env, put, run
from os.path import exists
from datetime import datetime
from pathlib import Path
"""
    Package and deploy the web application to the web servers.
    """


# Define the target hosts and SSH username
env.hosts = ['100.26.167.18', '54.175.189.193']
env.user = 'ubuntu'


def do_pack():
    """
    Create a compressed archive of the web_static directory.

    This function creates a timestamped compressed archive of the
    "web_static" directory and stores it in the "versions" directory.

    Returns:
        str: The path to the created archive, or None on failure.
    """
    try:
        # Create a "versions" directory if it doesn't exist
        local("mkdir -p versions")

        # Get the current timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Define the archive name
        archive_name = "web_static_" + timestamp + ".tgz"

        # Create the compressed archive
        local("tar -czvf versions/{} web_static".format(archive_name))

        archive_path = "versions/{}".format(archive_name)
        if exists(archive_path):
            return archive_path
        return None
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy a web application archive to the web servers.

    This function uploads a web application archive to the web servers,
    extracts it to the appropriate directory, and updates symbolic links.

    Args:
        archive_path (str): The path to the archive file on the local machine.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the web servers
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/<archive_basename>
        archive_filename = archive_path.split("/")[-1]
        archive_basename = Path(archive_filename).stem
        release_dir = "/data/web_static/releases/{}".format(archive_basename)
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_dir))

        # Delete the uploaded archive from /tmp/
        run("rm /tmp/{}".format(archive_filename))

        # Remove the current symbolic link if it exists
        current_link = "/data/web_static/current"
        if exists(current_link):
            run("rm {}".format(current_link))

        # Create a new symbolic link to the new version
        run("ln -s {} {}".format(release_dir, current_link))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False


def deploy():
    """
    Package and deploy the web application to the web servers.

    This function creates an archive of the web application and deploys it
    to the web servers. It returns True if deployment is successful,
    or False otherwise.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
