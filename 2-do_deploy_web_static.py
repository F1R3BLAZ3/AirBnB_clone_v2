#!/usr/bin/python3
"""
Fabric script that distributes an archive to your
web servers, using the function do_deploy
"""

from fabric.api import *
from os.path import exists
from datetime import datetime

env.hosts = ['34.237.91.138', '34.203.38.155']


@task
def do_pack():
    """
    based on this script
    """
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = f"versions/web_static_{formatted_dt}.tgz"
    print(f"Packing web_static to versions/web_static_{formatted_dt}.tgz")
    if local(f"{mkdir}&& tar -cvzf {path} web_static").succeeded:
        return path
    return None


@task
def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    try:
        if os.path.exists(archive_path) is False:
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run(f"rm -rf {dpath}{fn_no_ext}/")
        run(f"mkdir -p {dpath}{fn_no_ext}/")
        run(f"tar -xzf /tmp/{fn_with_ext} -C {dpath}{fn_no_ext}/")
        run(f"rm /tmp/{fn_with_ext}")
        run(f"mv {dpath}{fn_no_ext}/web_static/* {dpath}{fn_no_ext}/")
        run(f"rm -rf {dpath}{fn_no_ext}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {dpath}{fn_no_ext}/ /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
