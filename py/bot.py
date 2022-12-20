#imports
import bin.version as version
import modules.main as main
import sys
import os
import configparser
import wget
import shutil

#funky stuff to deal with relative file paths
randir = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

main.run()