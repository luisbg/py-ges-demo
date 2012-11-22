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
from gi.repository import Gst, GstPbutils
from gi.repository import GES
from gi.repository import GObject

class Engine():
    '''Interface class to Gst-Editing-Services'''

    def __init__(self):
        '''Initialize the Python class'''
        GES.init()    # we need to init GES for it to work

        self.timeline = GES.Timeline()   # create the central object of the Timeline
        self.pipeline = GES.TimelinePipeline()   # convenience class to render the Timeline
                                                 # handles the clock, bus and other things for us
        self.bus = self.pipeline.get_bus()
        self.pipeline.add_timeline(self.timeline)    # we need to add the Timeline into the Pipeline

        GES.Timeline.__init__(self.timeline)    # initialize the Timeline

        self.audio = GES.Track.audio_raw_new()    # we will have one raw Audio Track
        self.video = GES.Track.video_raw_new()    # and one raw Video Track

        self.timeline.add_track(self.audio)    # we add the Tracks to the Timeline
        self.timeline.add_track(self.video)

        Gst.init(None)    # we need to initialize Gst for it to work


    def add_file(self, file_uri):
        '''Function to add a file to the timeline'''
        src = GES.TimelineFileSource(uri=file_uri)    # we create a TimelineObject from the File
        src.set_priority(0)    # we add it to the bottom of the Timeline

        layer = GES.TimelineLayer()    # we create a new TimelineLayer
        layer.add_object(src)          # which will contain the new TimelineObject
        self.timeline.add_layer(layer)    # so we can add it to the Timeline

        disc = GstPbutils.Discoverer.new (50000000000)   # we discover the duration of the file
        info = disc.discover_uri (file_uri)

        # return the duration of the clip and the pointer to the TimelineObject
        return info.get_duration(), src

    def play(self):
        '''Method to change the state of the Pipeline to Playing'''
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        '''Method to change the state of the Pipeline to Ready'''
        self.pipeline.set_state(Gst.State.READY)

    def change_object_duration(self, tlobj, duration):
        '''Method to change the duration of the TimelineObject'''
        tlobj.set_duration(duration)

    def change_object_start(self, tlobj, start):
        '''Method to change the starting position of the TimelineObject'''
        tlobj.set_start(start)

    def change_object_inpoint(self, tlobj, in_point):
        '''Method to change the in point to play in the TimelineObject'''
        tlobj.set_inpoint(in_point)

    def change_object_priority(self, tlobj, priority):
        '''Method to change the priority of the TimelineObject inside its TimelineLayer'''
        tlobj.set_priority(priority)

    def prioritize(self, in_obj):
        '''Method to raise the priority of the TimelineObject to the top'''
        # prioritize selected object by changing its priority to 1 and the rest
        #   to 0
        for layer in self.timeline.get_layers():    # we run through the TimelineLayers
            for obj in layer.get_objects():         # check if the objects inside the TimelinLayers
                #print "obj uri ", obj.get_properties("uri")
                if obj is in_obj:                   # are the selected TimelineObject, and if they are
                    self.change_object_priority(obj, 0)
                else:                               # we change priority up to 1 or set back to 0
                    self.change_object_priority(obj, 1)
