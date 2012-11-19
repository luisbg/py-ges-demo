#!/usr/bin/env python

# -*- coding: utf-8 -*-
# PiTiVi , Non-linear video editor
#
#       engine.py
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

class Engine():

    def __init__(self):
        GES.init()

        self.timeline = GES.Timeline()
        self.pipeline = GES.TimelinePipeline()
        self.bus = self.pipeline.get_bus()
        self.pipeline.add_timeline(self.timeline)

        GES.Timeline.__init__(self.timeline)

        self.audio = GES.Track.audio_raw_new()
        self.video = GES.Track.video_raw_new()

        self.timeline.add_track(self.audio)
        self.timeline.add_track(self.video)

        self.layer = GES.SimpleTimelineLayer()
        self.timeline.add_layer(self.layer)

    def add_file(self, uri):
        src = GES.TimelineFileSource(uri=uri)
        src.set_property("priority", 1)
        self.layer.add_object(src, 0)

    def play(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.READY)
