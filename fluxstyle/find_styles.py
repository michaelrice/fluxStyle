# Copyright 2005-2014 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


"""Module to install, remove, and set styles for fluxbox"""

import tarfile
import re
import os
from os.path import expanduser
from os import system
from shutil import rmtree, copyfile
from sys import stdout


def set_style(style, location):
    """Select style and create entry in init file to reflect,
    then restart flux for change to take place
    """
    if location == "default":
        location = "~/.fluxbox/styles"
    location = expanduser(location)
    new_style_name = "session.styleFile:\t{0}/{1}\n".format(location, style)
    old_style_name = ""
    local_init = expanduser("~/.fluxbox/init")
    backup_init = expanduser("~/.fluxbox/init.bckp")
    copyfile(local_init, backup_init)
    init_file = open(backup_init,"r")
    init_file_lines = init_file.readlines()
    init_file.close()
    init_file_backup = open(backup_init, "r")
    style_line = re.compile(r"session.styleFile")
    for line in init_file_lines:
        if style_line.search(line):
            old_style_name = line
    output = stdout
    output =  open(local_init, "w")
    for line in init_file_backup.readlines():
        output.write(line.replace(old_style_name, new_style_name))
    output.close()
    init_file_backup.close()
    # attempt to not have to make a seperate fedora package for odd name
    # 'fluxbox-bin'
    system('kill -s USR2 `xprop -root _BLACKBOX_PID | awk \'{print $3}\'`')
    return

def install_style(style_file):
    """Install a valid tar.gz or tar.bz2 style foo.tar.gz/foo.tar.bz2 we
    check to see if it was  packaged as styleFoo/ or
    as ~/.fluxbox/styles/styleFoo people package both ways
    """
    for i in style_file:
        ins_dir = expanduser("~/.fluxbox/styles")
        if tarfile.is_tarfile(i) == True:
            # try first for bz2
            try:
                tar = tarfile.open(i, "r:bz2")
                #maybe its tar.gz
            except tarfile.ReadError:
                try:
                    tar = tarfile.open(i, "r:gz")
                    #this isnt a bz2 or gz, so wtf is it?
                except tarfile.ReadError:
                    #now return 2 to say weird file type..
                    #TODO: create exception class and rasie that
                    return False
            #we need to find out how the style was packaged
            #if it is ~/.fluxbox/styles/styleName then we need a new
            #install dir. otherwise use default.
            check = tar.getnames()
            pat = re.compile('^\.fluxbox/styles/.+')
            if pat.match(check[0]) == None:
                for i in tar:
                    tar.extract(i, ins_dir)
            else:
                ins_dir = expanduser("~/")
                for i in tar:
                    tar.extract(i, ins_dir)

        else:
            # 2 == it wasnt even a tar file at all. This is a double check,
            # we filter the file types in the file chooser to allow only
            # tar.gz and tar.bz2
            #TODO: raise an exception instead
            return 2
    return

def remove_style(style_file, location):
    """This can be used to remove a style"""
    if location == "default":
        location = "~/.fluxbox/styles"
    location = expanduser(location)
    if os.access(location + "/" + style_file, os.W_OK):
        rmtree(location + "/" + style_file)
        return True
    else:
        #TODO: raise exception here
        return False
