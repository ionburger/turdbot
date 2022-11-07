#imports
import version
import sys
import os
import configparser
import wget
import shutil

#funky stuff to deal with relative file paths
randir = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read("config.conf")
if config["config"]["autoupdate"] == "true":
    versionl = version.local()
    versionr = version.remote()
    if ".".join(versionl)<".".join(versionr):
        print("outdated version",versionl,"<",versionr)
        if config["config"]["autoupdate"] == "true":
            print("autoupdate is enabled, attempting to update")
            wget.download("https://github.com/ionburger/turdbot/archive/refs/tags/"+versionr+".zip",out = "turdbottmp.zip")
            shutil.unpack_archive("turdbottmp.zip","turdbottmp")
            for file in os.listdir("turdbottmp/turdbot-"+versionr+"/py/"):
                if file.endswith(".py"):
                    shutil.move("turdbottmp/turdbot-"+versionr+"/py/"+file,file)
            with open("VERSION","w") as file:
                file.write(versionr)
            shutil.rmtree("turdbottmp")
            os.remove("turdbottmp.zip")
            os.chdir(randir)
            os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        print("running latest version of turdbot",versionl)
