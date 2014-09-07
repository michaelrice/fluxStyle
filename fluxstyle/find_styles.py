# Copyright 2005 Michael Rice
# errr@errr-online.com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Module to install remove and set styles for fluxbox"""

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
