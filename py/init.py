import version
import sys
import os
if version.local() < version.remote():
    print("needs update")
else:
    print("is fine")
if input("aaa") == "y":
    os.execl(sys.executable, sys.executable, *sys.argv)
