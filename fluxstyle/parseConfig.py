'''Written by Michael Rice
Copyright Nov 14, 2005
Released under the terms of the GNU GPL v2
Email: Michael Rice errr@errr-online.com
Website: http://errr-online.com/
'''
import os,re
from os.path import expanduser

def check4_config():
    folder = expanduser("~/")
    file = folder+".fluxStyle.rc"
    w_ok = os.access(folder, os.W_OK)
    f_ok = os.path.isfile(file)
    if f_ok:
        return True
    elif not f_ok and w_ok:
        write_config()
        return 2
    #file isnt there and we dont have premission to make it.    
    elif not w_ok and not f_ok:
        return 3

def write_config():
    conFile = """
# No need to add ~/.fluxbox/styles it is the default location and if it is listed it will
# be ignored. Currently the only option supported right now is STYLES_DIRS
# to choose the name that will display in the view menu use the following syntax
# Name,/location:Foo,/other/location:Bar,/another/location
# If the name identifier is left off "Extra Styles" will be used.
# The following line is an example of what to use if you have styles installed in these places
#STYLES_DIRS:Global,/usr/share/fluxbox/styles:Tenners,/usr/share/tenr-de-styles-pkg-1.0/styles/
"""
    file = expanduser("~/.fluxStyle.rc")
    file = open(file, "w")
    file.write(conFile)
    file.close()
#    return 2

def parse_file(file):
    """read config file place results into a 
    dict file location provided by caller. 
    keys = options (USEICONS, ICONPATHS, etc)
    values = values from options
    config file should be in the form of:
    OPTION:values:moreValuse:evenMore
    do not end with ":"  Comments are "#" as 
    the first char.
    #OPTION:commet
    OPTION:notComment #this is not valid comment
    """
    file = expanduser(file)
    opts = {}
    if os.path.isfile(file):
        match = re.compile(r"^[^#^\n]")
        f = open(file)
        info = f.readlines()
        f.close()
        keys = []
        for lines in info:
            if match.findall(lines):
                keys.append( lines.strip().split(":") )
        if len(keys) == 0:
            return False
        for i in range(len(keys)):
            opts[keys[i][0]] = keys[i][1:]
        return opts
    else:
        return False    
if __name__ == "__main__":
    #print parse_file("~/.fluxStyle.rc")
    x = parse_file("~/.fluxStyle.rc")
    l = []
    for k,v in x.iteritems():
      if k == "STYLES_DIRS":
        for i in v:
          l.append( i.strip().split(",") )
        for i in l:
          if len(i) <= 1:
            print "default ", i[0]
          else:
            print i[0], i[1]
