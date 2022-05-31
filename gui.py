#!/usr/bin/python3

import gi
import meta
from os import system
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class rootWindow(Gtk.Window):

    def __init__(self, shouldCloseAfterCopying, clipboardMethod):

        self.shouldCloseAfterCopying = shouldCloseAfterCopying

        if clipboardMethod == "xsel" and system("which xsel") != 0:
            print("CLIPBOARD_METHOD xsel was selected but xsel is not found on the system.")
            sys.exit(1)

        self.clipboardMethod = clipboardMethod

        super().__init__(title = meta.constants.ROOTWINDOW_TITLE)

        self.set_default_size(meta.constants.ROOTWINDOW_WIDTH, meta.constants.ROOTWINDOW_HEIGHT)

        self.mainVbox = Gtk.Box(orientation="vertical")

        self.mojiSearch = Gtk.Entry()

        self.mojiSearch.connect("changed", self._onEntryChanged) #use entry to filter mojilist

        self.mojiListContainer = Gtk.ScrolledWindow()

        self.mojiListStore = Gtk.ListStore(str, str)

        self.mojiListFilter = self.mojiListStore.filter_new()

        self.mojiListFilter.set_visible_func(self._mojiFilter, data=None)

        self.mojiListView = Gtk.TreeView(model=self.mojiListFilter)

        self.mojiListView.append_column(Gtk.TreeViewColumn(cell_renderer=Gtk.CellRendererText(), text=1))

        listSelection = self.mojiListView.get_selection()
        listSelection.connect("changed", self._onSelectionChanged) #copy on mojilist selection

        self.mojiListContainer.add(self.mojiListView)

        self.mainVbox.pack_start(self.mojiSearch, False, False, 0)
        self.mainVbox.pack_end(self.mojiListContainer, True, True, 0)

        self.add(self.mainVbox)

        if self.clipboardMethod == "gtk":
            self.clipboard = Gtk.Clipboard().get(Gdk.SELECTION_CLIPBOARD)

        self.connect("destroy", Gtk.main_quit)
        self.connect("key_press_event", self._onWindowKeypress) #close on escape press

        self.show_all()

    def _onWindowKeypress(self, window, event):

        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        else:
            return False

    def _onSelectionChanged(self, selection):

        model, iterObject = selection.get_selected()

        if iterObject:
            if self.clipboardMethod == "gtk":
                self._copyToClipboardGtk(f"{model[iterObject][1]}")
            else: 
                self._copyToClipboardXsel(f"{model[iterObject][1]}")

            if self.shouldCloseAfterCopying:
                Gtk.main_quit()

    def _onEntryChanged(self, entryObject):

        self.mojiListFilter.refilter()

    def _mojiFilter(self, model, iterObject, data=None):

        text = self.mojiSearch.get_text()
        if text != "":
            return text in model[iterObject][0]
        else:
            return True

    def _copyToClipboardXsel(self, text):

        system(f"echo -n -E '{text}' | xsel -i -b")

    def _copyToClipboardGtk(self, text):

        self.clipboard.set_text(text, -1)
        self.clipboard.set_can_store(None)
        self.clipboard.store()

    def populate(self, mojiList):

        try:
            for name, moji in mojiList.items():

                self.mojiListStore.append((name, moji))

            self.show_all()
        except Exception as e:
            print("something bad with list!!（　ﾟДﾟ）")
            print(e)
            print("quitting... (҂◡_◡)")
            Gtk.main_quit()
