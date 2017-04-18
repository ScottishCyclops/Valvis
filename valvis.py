#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
    "Valvis" is a blender project manager
    Copyright (C) 2017 Scott Winkelmann <scottlandart@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import getopt
import json
import os

MAJOR = 1
MINOR = 0
FIX = 0

CONFIG = {}
HOME = ""
CONFIG_FOLDER = ""
CONFIG_FILE = "config.json"
CONFIG_FILE_PATH = ""

def checkNoParamError(index, opts):
    if index > len(opts):
        print("please provide a parameter")
        print(opts)
        sys.exit(1)

def createDefaultConfig():
    #TODO: ask user for other infos
    defaultConfig = {"projects_path" : HOME+"/Documents/valvis"}
    json.dump(defaultConfig,open(CONFIG_FILE_PATH, "w+"))

def loadConfig():
    global CONFIG
    global HOME
    global CONFIG_FOLDER
    global CONFIG_FILE_PATH

    HOME = os.path.expanduser("~")
    CONFIG_FOLDER = HOME+"/.config/valvis"
    CONFIG_FILE_PATH = CONFIG_FOLDER+"/"+CONFIG_FILE

    if os.path.isdir(HOME):
        if not os.path.exists(CONFIG_FOLDER):
            os.makedirs(CONFIG_FOLDER)
            createDefaultConfig()
    else:
        print("couldn't find user folder")
        sys.exit(1)

    CONFIG = json.load(open(CONFIG_FILE_PATH, "r"))

def helpCmd(full = False):
    print("usage: valvis.py [--version] [--help] [--new <project name>]")
    if full:
        print("\ninformation commands :")
        print("  version    prints software version")
        print("  help       prints this help message\n")
        print("\nproject commands :")
        print("  new       creates a new project")
        print("  save      creates a full save of current project state")
        print("  backup    reverts a file to it's last saved state\n")
        print("\nconfiguration commands :")
        print("  config     sets a config parameter\n")

def versionCmd():
    print("valvis version {0}.{1}.{2}".format(MAJOR,MINOR,FIX))

def newCmd(newProjectName):
    newProjectPath = CONFIG["projects_path"]+"/"+str(newProjectName)
    if os.path.exists(newProjectPath):
        print("a project with this name already exists")
        sys.exit(1)
    else:
        '''taking all informations before doing anything'''
        newProjectDesc = input("Enter a short description for '{0}': ".format(newProjectName))

        #document structure
        os.makedirs(newProjectPath)
        os.makedirs(newProjectPath+"/1_blends")
        os.makedirs(newProjectPath+"/2_textures")
        os.makedirs(newProjectPath+"/3_references")
        os.makedirs(newProjectPath+"/4_documents")
        os.makedirs(newProjectPath+"/5_renders")
        os.symlink(CONFIG['library_path'],newProjectPath+"/6_library")
        os.makedirs(newProjectPath+"/.valvis")

        #readme
        newProjectReadMe = "# {0}\n\n{1}\n".format(newProjectName,newProjectDesc)
        if CONFIG['user_name'] != -1:
            newProjectReadMe+="\nCreated by {}".format(CONFIG['user_name'])
            if CONFIG['user_email'] != -1:
                newProjectReadMe+=" - <{}>".format(CONFIG['user_email'])
        newProjectReadMe+="\n\n## Copyright notice:\n\n\
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.\n\n\
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."

        with open(newProjectPath+"/README.md","w+") as f:
            f.write(newProjectReadMe)

        #default blender file

        
        #confirmation
        print("project '{0}' was successfully created under '{1}'".format(newProjectName,newProjectPath))


def main():
    if(len(sys.argv) == 1):
        helpCmd()
        sys.exit(0)
    try:
        #we omit first arg because it's always the script name
        opts, args = getopt.getopt(sys.argv[1:], "hvn:", ["help", "version", "new="])
    except getopt.GetoptError as err:
        print(str(err))
        helpCmd()
        sys.exit(2)

    loadConfig()

    for o, a in opts:
        if o in ("-h", "--help"):
            helpCmd(True)
            sys.exit(0)
        elif o in ("-v", "--version"):
            versionCmd()
            sys.exit(0)
        elif o in ("-n", "--new"):
            newCmd(a)
            sys.exit(0)

if __name__ == "__main__":
    main()
