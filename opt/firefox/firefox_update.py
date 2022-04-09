#!/usr/bin/python3
import time

import requests
import re
import subprocess
import tarfile
import os
import psutil


def get_latest_version():
    """Get latest version of firefox"""
    try:
        r = requests.head("https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US")
    except Exception as e:
        print(f"Error while check new version... Error: {e}")
        exit(1)
    if r.status_code == 302:
        link = r.headers['Location']
        version_re = re.search("releases/.*/linux-x86_64", link)
        version = version_re.group(0).split('/')[1]
        return link, version
    else:
        print(f"Status codes not OK while checking new version. Status code: {r.status_code}")
        exit(1)


def get_current_version():
    """Return current version of installed firefox"""
    firefox_run = subprocess.run([f"{os.environ['firefox_path']}firefox/firefox", '--version'], stdout=subprocess.PIPE)
    firefox_installed_version = firefox_run.stdout.decode().rstrip().split(" ")[2]
    return firefox_installed_version


def download_firefox_archive(link, latest_version):
    """Download latest firefox version and save to /tmp/"""
    print("Downloading latest version...")
    try:
        r = requests.get(link , stream=True)
    except Exception as e:
        print(f"Error while download... Exception: {e}")
        exit(1)
    if r.status_code == requests.codes.ok:
        firefox_file = open(f"/tmp/{latest_version}.tar.bz2", "wb")
        try:
            for current_chunk in r.iter_content(5242880):
                print("Chunk")
                firefox_file.write(current_chunk)
            firefox_file.close()
        except Exception as e:
            print(f"Error while downloading file. Exception: {e}")
            exit(1)
    else:
        print(f"Error when download... Status code: {r.status_code}")
        exit(1)


def find_running_firefox_pids():
    """Find main PID running firefox process"""
    processes_list = psutil.process_iter()
    for process in processes_list:
        if process.name() == "firefox-bin":
            print(f"Found firefox process. PID: {process.pid}")
            kill_running_firefox_instance(process)
            return None
    print("Running firefox not found")


def kill_running_firefox_instance(process):
    """Send SIGQUIT to firefox pid"""
    print("Going to kill firefox process. After we will sleep 10 seconds")
    try:
        process.send_signal(1)
    except Exception as e:
        print(f"Can not kill running Firefox instance. Error: {e}")
        exit(1)
    time.sleep(10)


def unpack_archive(latest_version):
    """Unpack archive"""
    print("Unpacking archive...")
    tar_file = tarfile.open(f"/tmp/{latest_version}.tar.bz2", "r:bz2")
    tar_file.extractall(f"{os.environ['firefox_path']}")
    tar_file.close()
    print("Completed")


latest_version_link, latest_version = get_latest_version()
my_version = get_current_version()

if latest_version == my_version:
    print(f"You have latest version: {my_version}")
else:
    print(f"New version released! Your version: {my_version}, latest version: {latest_version}")
    download_firefox_archive(latest_version_link, latest_version)
    find_running_firefox_pids()
    unpack_archive(latest_version)
    print("Exiting... Bye!")
