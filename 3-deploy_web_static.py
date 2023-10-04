from fabric.api import *
from os.path import exists
import time

env.hosts = ['34.237.91.138', '34.203.38.155']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """

    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create a timestamped filename
    t = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    filename = "versions/web_static_{}.tgz".format(t)

    # Use tar to create the archive
    result = local("tar -cvzf {} web_static".format(filename))

    # Return the archive path if successful, otherwise None
    return filename if result.succeeded else None

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """

    # Check if the file at the path archive_path exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        
        # Get the file name without extension
        file_name = archive_path.split("/")[-1]
        name = file_name.replace(".tgz", "")
        
        # Uncompress the archive to the folder /data/web_static/releases/
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name))
        
        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        
        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")
        
        # Create a new symbolic link /data/web_static/current on the web server
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        
        return True
    except:
        return False

def deploy():
    """
    Creates and distributes an archive to web servers
    """

    # Call do_pack() and store the path of the created archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if archive_path is None:
        return False

    # Call do_deploy() with the new path of the new archive
    return do_deploy(archive_path)

