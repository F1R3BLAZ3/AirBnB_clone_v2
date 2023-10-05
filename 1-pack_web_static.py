#!/usr/bin/python3
"""
script that generates a .tgz archive from the contents of the web_static
"""


from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Create a compressed archive of the web_static folder.

    This function generates a timestamp and creates a compressed archive
    of the web_static folder with a name like "web_static_<timestamp>.tgz".
    The archive is stored in the "versions" directory.

    Returns:
        str: The path to the created archive, or None if an error occurs.
    """
    try:
        # Get the current timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Define the archive name
        archive_name = "web_static_" + timestamp + ".tgz"

        # Create the "versions" directory if it doesn't exist
        local("mkdir -p versions")

        # Create the compressed archive
        local("tar -czvf versions/{} web_static".format(archive_name))

        # Return the path to the created archive
        return "versions/{}".format(archive_name)
    except Exception:
        # Return None in case of an error
        return None
