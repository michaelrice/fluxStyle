#!/usr/bin/env python
#
# Fluxstyle is a graphical style manager built in python
# using pygtk and glade. Fluxstyle is for the fluxbox window
# manager. Orignal version written by Michael Rice. Many special
# thanks to Zan a.k.a. Lauri Peltonen for GUI Improvements & Bug Stomping.

from __future__ import print_function

from distutils.core import setup
import distutils.fancy_getopt
import sys

DATADIR = "/usr/share"
BINDIR = "/usr/bin"


def chk_install():
    """try to pull in gtk crap to make sure deps are on box before install"""
    ver = sys.version[:5]
    try:
        import gtk
    except:
        print("You seem to be missing gtk bindings for python")
        print("Please install them before you install fluxstyle")
        print("http://pygtk.org/")
        raise SystemExit
    try:
        import gtk.glade
    except:
        print("You need to install libglade2")
        raise SystemExit
    if gtk.pygtk_version < (2, 3, 90):
        print("PyGtk 2.3.90 or later required for this program")
        print("It is recommended that you get pygtk 2.6 or newer.")
        raise SystemExit


def main():
    chk_install()
    doclines = __doc__.split("\n")
    setup(
        name='fluxstyle',
        version='1.2',
        description=doclines[0],
        author='Michael Rice',
        author_email='errr@errr-online.com',
        url='https://github.com/michaelrice/fluxStyle/',
        packages=['fluxstyle'],
        data_files=[
            (
                DATADIR + '/fluxstyle/images', [
                    'images/fluxmetal.png',
                    'images/mini-fluxbox6.png',
                    'images/none.jpg'
                ]
            ),
            (DATADIR + '/fluxstyle/glade', ['images/main.glade']),
            (BINDIR, ['fluxstyle_gui']),
            (DATADIR + '/fluxstyle/docs',
             ['docs/README', 'docs/LICENSE', 'docs/Changelog'])
        ]
    )


if __name__ == "__main__":
    main()
