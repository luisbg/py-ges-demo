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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gst
from gi.repository import GES
from gi.repository import GObject

class Demo():

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.curdir, "ui.glade"))
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window")
        self.window.connect("delete-event", self.quit)
        self.window.show_all()

    def quit(self, unused_window=None, unused_even=None):
        Gtk.main_quit
        exit(0)

demo = Demo()
Gtk.main()
