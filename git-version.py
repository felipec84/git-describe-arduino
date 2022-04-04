#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script to provide automatic git-base versioning to Arduino's sketches.
# Basically it runs "git describe" on source folder and creates 
# a file in the destination directory containg an elaborated output.
# If output is not found in source directory, the script ends immediatly
# without errors.
# (by default, output file is named git-version.h)
#
# Input parameters:
#  1. [Mandatory] source folder, where target files is located. It may be in subfolder of repository.
#  2. [Optional] (Default value: the same as first param) path of destination directory.

# Name of file that is created
from sys import argv, exit
import os
from os.path import exists
from pathlib import Path
from subprocess import check_output

filename='git-version.h'

# Go to the source directory
if len(argv) > 1 and len(argv[1]) > 0:
    os.chdir(argv[1])
else:
    print("You MUST specify the first param. Exiting...")
    exit(1)
print("Executing source path = ", argv[1])

filepath = Path(argv[1]) / filename
if exists(filepath):
    print(str(filepath)+" exist")
else:
    print(str(filepath)+" not exist")
    exit(0)

if len(argv) > 2 and len(argv[2]) > 0:
    filepath=Path(argv[2]) / filename
else:
    filepath=Path('.') / filename

# Build a version string with git
version=check_output(['git', 'describe', '--tags', '--always', '--dirty'], stderr=None, encoding='ascii')
version = version.strip()

if ( len(version) != 0):
    print("git version:" + version)
else:
    print("No git repo was found!")
    exit(1)

# If this is not a git repository, fallback to the compilation date
#[ -n "$version" ] || version=$(date -I)
# If this is not a git repository, create an empty file
#[ -n "$version" ] || echo "" > $filename; exit 1

# Save this in git-version.h
print("Creating file " + str(filepath) + "...", end=None)
filepath.write_text(f"#define GIT_VERSION \"{version}\"")
print(" Done!")

#read -p "Press key to exit..." variable1