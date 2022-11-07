#imports
import version
import sys
import os

#funky stuff to deal with relative file paths
dir = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#updater
if version.local() < version.remote():
    print("needs update")
else:
    print("is fine")
if input("aaa") == "y":
    
    os.chdir(dir)
    os.execl(sys.executable, sys.executable, *sys.argv)
