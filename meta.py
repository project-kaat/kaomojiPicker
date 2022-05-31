#!/usr/bin/python3

class constants:

    ROOTWINDOW_TITLE            = "kaomoji picker"

    ROOTWINDOW_WIDTH            = 300
    ROOTWINDOW_HEIGHT           = 300

class settings:

    """
    Whether the window should destroy itself after
    an element was chosen from the list.
    Disable this if your clipboard gets cleared upon exiting the program
    when using CLIPBOARD_METHOD="gtk"
    """
    CLOSE_AFTER_COPYING         = True

    """
    Method of accessing the clipboard to paste your
    choosen kaomoji.
    Possible values:
        xsel        - default. requires xsel
        gtk         - native gtk. unreliable for some reason
    """
    CLIPBOARD_METHOD            = "xsel"
#    CLIPBOARD_METHOD            = "gtk"
