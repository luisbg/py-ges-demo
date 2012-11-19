#!/usr/bin/env python

# -*- coding: utf-8 -*-
# PiTiVi , Non-linear video editor
#
#       ui.py
#
# Copyright (c) 2012 Luis de Bethencourt <luis.debethencourt@collabora.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.

import os
import random

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gst
from gi.repository import GES
from gi.repository import GObject

class Demo():

    def __init__(self):
        self.clips = {}

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.curdir, "ui.glade"))
        self.builder.connect_signals(self)

        self.timeline_treeview = self.builder.get_object("timeline_treeview")
        self.timeline_store = Gtk.ListStore(str, str, str, str)
        self.timeline_treeview.set_model(self.timeline_store)
        self.timeline_current_iter = None        #To keep track of the cursor

        self.start_entry = self.builder.get_object("start_entry")
        self.duration_scale = self.builder.get_object("duration_scale")
        self.in_point_scale = self.builder.get_object("in_point_scale")

        self.window = self.builder.get_object("window")
        self.window.show_all()

    def add_file(self, filepath):
        uri = Gst.filename_to_uri (filepath)
        v = {}
        for a in range(0, 2):
            v[a] = str(random.randint(0,1000))
        self.timeline_store.append([uri, "0", v[0], v[1]])
        self.clips[uri] = ("0", v[0], v[1])

    def _clip_selected(self, widget):
        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        if row_iter is None:
            return

        uri = self.timeline_store.get_value(row_iter, 0)
        print "active clip: ", uri, self.clips[uri]

        self._update_properties_box(uri)

    def _update_properties_box(self, uri):
        clip = self.clips[uri]
        self.start_entry.set_text(clip[0])
        self.duration_scale.set_range(0, 1000)
        self.duration_scale.set_value(int(clip[1]))
        self.in_point_scale.set_range(0, 1000)
        self.in_point_scale.set_value(int(clip[2]))

    def _stop_activate_cb(self, widget):
        print "stop"

    def _play_activate_cb(self, widget):
        print "play"

    def _move_up_activate_cb(self, widget):
        print "move up"

    def _move_down_activate_cb(self, widget):
        print "move down"

    def _add_file_activated_cb(self, widget):
        filechooser = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN,
                      buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = filechooser.run()
        if response != Gtk.ResponseType.OK:
            filechooser.destroy()
            return

        filepath = filechooser.get_filename()
        if filepath and os.access(filepath, os.R_OK):
            filechooser.destroy()
            self.add_file(filepath)

    def _delete_activate_cb(self, widget):
        print "delete"

    def _duration_scale_change_value_cb(self, widget, a, b):
        print "duration scale change"

    def _in_point_scale_change_value_cb(self, widget, a, b):
        print "in point scale change value"

    def _window_delete_event_cb(self, unused_window=None, unused_even=None):
        Gtk.main_quit
        exit(0)

demo = Demo()
Gtk.main()
