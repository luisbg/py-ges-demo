#!/usr/bin/env python

# -*- coding: utf-8 -*-
# PiTiVi , Non-linear video editor
#
#       py-ges-demo.py
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

from engine import Engine

class GesDemo():

    def __init__(self):
        self.engine = Engine()

        self.clips = {}

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.curdir, \
            "py-ges-demo.glade"))
        self.builder.connect_signals(self)

        self.timeline_treeview = self.builder.get_object("timeline_treeview")
                                            #id, uri, start, duration, in point
        self.timeline_store = Gtk.ListStore(int, str, long, long, long)
        self.timeline_treeview.set_model(self.timeline_store)
        self.timeline_current_iter = None        #To keep track of the cursor

        self.start_entry = self.builder.get_object("start_entry")
        self.duration_scale = self.builder.get_object("duration_scale")
        self.in_point_scale = self.builder.get_object("in_point_scale")

        self.window = self.builder.get_object("window")
        self.window.show_all()

    def add_file(self, filepath):
        idf = len(self.clips)

        uri = Gst.filename_to_uri (filepath)
        duration = self.engine.add_file(uri)

        self.timeline_store.append([idf, os.path.basename(filepath), 0,
                                   duration, 0])
        # clips[id] = uri, start, duration, in_point, max_duration
        self.clips[idf] = [uri, 0, duration, 0, duration]

    def _clip_selected(self, widget):
        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        if row_iter is None:
            return

        idf = self.timeline_store.get_value(row_iter, 0)
        print "active clip: ", self.clips[idf]

        self._update_properties_box(idf)

    def _update_properties_box(self, idf):
        clip = self.clips[idf]
        self.start_entry.set_text(str(clip[1]))
        self.duration_scale.set_range(0, clip[4] - clip[3])
        self.duration_scale.set_value(clip[2])
        self.in_point_scale.set_range(0, clip[4])
        self.in_point_scale.set_value(clip[3])

    def _stop_activate_cb(self, widget):
        self.engine.stop()

    def _play_activate_cb(self, widget):
        self.engine.play()

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

    def _start_changed(self, widget):
        new_start = widget.get_text()
        print "new start entered", new_start

        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        idf = self.timeline_store.get_value(row_iter, 0)
        self.clips[idf][1] = new_start
        try:
            self.timeline_store.set_value(row_iter, 2, long(new_start))
        except:
            self.timeline_store.set_value(row_iter, 2, 0)

    def _duration_scale_change_value_cb(self, widget, event):
        new_duration = widget.get_value()
        print "duration scale change", new_duration

        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        idf = self.timeline_store.get_value(row_iter, 0)
        self.clips[idf][2] = new_duration
        self.timeline_store.set_value(row_iter, 3, long(new_duration))

    def _in_point_scale_change_value_cb(self, widget, event):
        new_in_point = widget.get_value()
        print "in point scale change value", new_in_point

        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        idf = self.timeline_store.get_value(row_iter, 0)
        self.clips[idf][3] = new_in_point
        self.timeline_store.set_value(row_iter, 4, long(new_in_point))

    def _window_delete_event_cb(self, unused_window=None, unused_even=None):
        Gtk.main_quit
        exit(0)

demo = GesDemo()
Gtk.main()
