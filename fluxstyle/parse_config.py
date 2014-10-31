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

from __future__ import print_function
import os
import re
from os.path import expanduser


def check4_config():
    """checks to see if the config file is located in the users home dir"""
    folder = expanduser("~/")
    config_file = folder+".fluxStyle.rc"
    w_ok = os.access(folder, os.W_OK)
    f_ok = os.path.isfile(config_file)
    if f_ok:
        return True
    elif not f_ok and w_ok:
        write_config()
        return 2
    #file isnt there and we dont have permission to make it.
    elif not w_ok and not f_ok:
        return 3


def write_config():
    """writes the basic config file in the users home dir"""
    config_file_text = """
# No need to add ~/.fluxbox/styles it is the default location and if it is listed it will
# be ignored. Currently the only option supported right now is STYLES_DIRS
# to choose the name that will display in the view menu use the following syntax
# Name,/location:Foo,/other/location:Bar,/another/location
# If the name identifier is left off "Extra Styles" will be used.
# The following line is an example of what to use if you have styles installed in these places
#STYLES_DIRS:Global,/usr/share/fluxbox/styles:Tenners,/usr/share/tenr-de-styles-pkg-1.0/styles/
"""
    config_file = expanduser("~/.fluxStyle.rc")
    config_file = open(config_file, "w")
    config_file.write(config_file_text)
    config_file.close()
#    return 2


def parse_file(config_file):
    """read config file place results into a
    dict file location provided by caller.
    keys = options (USEICONS, ICONPATHS, etc)
    values = values from options
    config file should be in the form of:
    OPTION:values:moreValuse:evenMore
    do not end with ":"  Comments are "#" as
    the first char.
    #OPTION:comment
    OPTION:notComment #this is not valid comment
    """
    config_file = expanduser(config_file)
    opts = {}
    if os.path.isfile(config_file):
        match = re.compile(r"^[^#^\n]")
        file_handle = open(config_file)
        info = file_handle.readlines()
        file_handle.close()
        keys = []
        for lines in info:
            if match.findall(lines):
                keys.append(lines.strip().split(":"))
        if len(keys) == 0:
            return False
        for i in range(len(keys)):
            opts[keys[i][0]] = keys[i][1:]
        return opts
    else:
        return False

if __name__ == "__main__":
    CFG = parse_file("~/.fluxStyle.rc")
    if not CFG:
        write_config()
        raise SystemExit("You need to edit the file ~/fluxStyle.rc")

    ITEMS = []
    for key, value in CFG.iteritems():
        if key == "STYLES_DIRS":
            for file_location in value:
                ITEMS.append(file_location.strip().split(","))
    for item in ITEMS:
        if len(item) <= 1:
            print("default {0}".format(item[0]))
        else:
            print("{0} {1}".format(item[0], item[1]))

