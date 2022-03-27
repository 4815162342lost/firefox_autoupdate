#!/usr/bin/python3
import requests
import re
import subprocess
import tarfile
import os

def get_latest_version():
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
    firefox_run = subprocess.run([f"{os.environ['firefox_path']}firefox/firefox", '--version'], stdout=subprocess.PIPE)
    firefox_istalled_version = firefox_run.stdout.decode().rstrip().split(" ")[2]
    return firefox_istalled_version

def download_firefox_archive(link, latest_version):
    print("Downloading latest version...")
    try:
        r = requests.get(link)
    except Exception as e:
        print(f"Error while download... Exception: {e}")
        exit(1)
    if r.status_code == requests.codes.ok:
        firefox_file = open(f"/tmp/{latest_version}.tar.bz2", "wb")
        firefox_file.write(r.content)
        firefox_file.close()
    else:
        print(f"Error while download new version, status code not 200. Status code: {r.status_code}")
        exit(1)

def unpack_archive(latest_version):
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
    unpack_archive(latest_version)
    print("Exiting... Bye!")
