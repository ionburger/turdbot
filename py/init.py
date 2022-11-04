#imports
import version
import sys
import os
import configparser
import wget
import sysrsync
import shutil

#funky stuff to deal with relative file paths
dir = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read("config.conf")
if config["config"]["autoupdate"] == "true":
    versionl = version.local()
    versionr = version.remote()

#updater
if versionl < versionr:
    print("outdated version detected\n",versionl," < ",versionr)
    if config["config"]["autoupdate"] == "true":
        print("autoupdate is enabled, attempting to update")
        wget.download("https://github.com/ionburger/turdbot/archive/refs/tags/"+versionr+".zip",out = "turdbot.zip")
        shutil.unpack_archive("turdbot.zip","turdbot")      
        sysrsync.run(source="turdbot/turdbot-"+versionr+"/py/*.py",destination="*.py")  
        os.chdir(dir)
        os.execl(sys.executable, sys.executable, *sys.argv)
else:
    print("running latest version of turdbot ",versionl)
