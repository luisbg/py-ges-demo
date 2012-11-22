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
    '''User Interface class'''
    def __init__(self):
        '''Initialize the User Interface and the GES Engine'''

        self.engine = Engine()

        self.clips = {}

        # we import the gtk objects from glade and create our GtkStore and TreeView
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

    def _clip_selected(self, widget):
        '''Method connected to the selection-changed signal of the TreeView'''
        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        if row_iter is None:
            self.engine.prioritize(None)
        else:
            idf = self.timeline_store.get_value(row_iter, 0)
            self.engine.prioritize(self.clips[idf][5])
            print "active clip: ", self.clips[idf]

            self._update_properties_box(idf)

    def _update_properties_box(self, idf):
        '''Method to update the properties box with the information of the selected clip'''
        clip = self.clips[idf]
        self.start_entry.set_text(str(clip[1]))
        self.duration_scale.set_range(0, clip[4] - clip[3])
        self.duration_scale.set_value(clip[2])
        self.in_point_scale.set_range(0, clip[4])
        self.in_point_scale.set_value(clip[3])

    def _play_activate_cb(self, widget):
        '''Method connected to the Play button'''
        self.engine.play()

    def _stop_activate_cb(self, widget):
        '''Method connected to the Stop button'''
        self.engine.stop()

    def _add_file_activated_cb(self, widget):
        '''Method connected to the Add File button'''
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

    def add_file(self, filepath):
        '''Method that adds the file to the GtkStore and GESTimeline'''
        idf = len(self.clips)    # id field is a counter

        uri = Gst.filename_to_uri (filepath)   # conver the filepath into a valid URI
        duration, tlobj = self.engine.add_file(uri)    # add the uri to the GESTimeline

        # add to the GtkStore and internal list
        self.timeline_store.append([idf, os.path.basename(filepath), 0,
                                   duration, 0])
        # clips[id] = uri, start, duration, in_point, max_duration, timelineobj
        self.clips[idf] = [uri, 0, duration, 0, duration, tlobj]

    def _delete_activate_cb(self, widget):
        '''Method connected to the Delete button'''
        print "delete"

    def _start_changed(self, widget):
        '''Method connected to the Changed event of the start entry'''
        new_start = widget.get_text()
        print "new start entered", new_start

        # find the selected clip
        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        idf = self.timeline_store.get_value(row_iter, 0)
        self.clips[idf][1] = new_start
        # set the new value to the Gtk TreeStore
        try:
            self.timeline_store.set_value(row_iter, 2, long(new_start))
        except:
            self.timeline_store.set_value(row_iter, 2, 0)
            new_start = 0

        # change the value of the GES TimelineObject
        self.engine.change_object_start(self.clips[idf][5], long(new_start))

    def _duration_scale_change_value_cb(self, widget, event):
        '''Method connected to the Changed event of the Duration scale'''
        new_duration = widget.get_value()
        print "duration scale change", new_duration

        # find the selected clip
        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        idf = self.timeline_store.get_value(row_iter, 0)
        self.clips[idf][2] = new_duration
        # set the new value to the Gtk TreeStore
        self.timeline_store.set_value(row_iter, 3, long(new_duration))

        # change the value of the GES TimelineObject
        self.engine.change_object_duration(self.clips[idf][5], new_duration)

    def _in_point_scale_change_value_cb(self, widget, event):
        '''Method connected to the Changed event of the In Point scale'''
        new_in_point = widget.get_value()
        print "in point scale change value", new_in_point

        # find the selected clip
        model, row_iter = self.timeline_treeview.get_selection().get_selected()
        idf = self.timeline_store.get_value(row_iter, 0)
        self.clips[idf][3] = new_in_point
        # set the new value to the Gtk TreeStore
        self.timeline_store.set_value(row_iter, 4, long(new_in_point))

        # change the value of the GES TimelineObject
        self.engine.change_object_inpoint(self.clips[idf][5], new_in_point)

    def _window_delete_event_cb(self, unused_window=None, unused_even=None):
        '''Method connected to the Delete event of the window'''
        Gtk.main_quit
        exit(0)


# Start the application
demo = GesDemo()
Gtk.main()
