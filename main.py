#!/usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import gui
from mojis import default
import meta

def main():

    rootWin = gui.rootWindow(meta.settings.CLOSE_AFTER_COPYING, meta.settings.CLIPBOARD_METHOD)
    rootWin.populate(default.res)

    Gtk.main()

if __name__ == "__main__":

    main()

