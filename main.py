#!/usr/bin/python3
import requests
import re
import subprocess
import tarfile

def get_latest_version(): 
    r = requests.head("https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US")
    link = r.headers['Location']
    version_re = re.search("releases/.*/linux-x86_64", link)
    version = version_re.group(0).split('/')[1]
    return link, version                  

def get_current_version():
    firefox_run = subprocess.run(['/opt/firefox/firefox/firefox', '--version'], stdout=subprocess.PIPE)
    firefox_istalled_version = firefox_run.stdout.decode().rstrip().split(" ")[2]
    return firefox_istalled_version

def download_firefox_archive(link, latest_version):
    r = requests.get(link)
    firefox_file = open(f"/tmp/{latest_version}.tar.bz2", "wb")
    firefox_file.write(r.content)
    firefox_file.close()

def unpack_archive(latest_version):
    tar_file = tarfile.open(f"/tmp/{latest_version}.tar.bz2", "r:bz2")
    tar_file.extractall("/tmp/firefox/")
    tar_file.close()

latest_version_link, latest_version = get_latest_version()
my_version = get_current_version()

if latest_version == my_version:
    print(f"You have latest version: {my_version}")
else:
    print(f"New version released! Your version: {my_version}, latest version: {lstest_version}")
    download_firefox_archive(latest_version_link, latest_version)
    unpack_archive(latest_version)
