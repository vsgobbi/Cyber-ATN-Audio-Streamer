
__author__ = 'vitor'


#! /usr/bin/env python
"""
Starting again from scratch, this time using Python Gstreamer 1.0,
by the fact didn't get any sucess trying to play a whole playlist using gst 0.10
-----------------------------------------------------------------------------------------------------------------------
July, 2015, Vitor Sgobbi
Brazilian Airspace Control Institute
Cyber Range ATN Testbed
This is where we play all the mp3 audio files from air traffic control, pilots and noise
The goals are: 1. To create a basic script player,
a client and server to stream mp3 audio in a loop without stopping the sink
2. TCP broadcast streaming
3. Create dynamic pipeplines
-----------------------------------------------------------------------------------------------------------------------
"""


import os, sys, random, pygtk, pygments, pygst
import gi, gobject
gi.require_version('Gst', '1.0')
#from gi.repository import GObject, Gst
from gobject import GObject
from pygst import __all__
GObject.threads_init()
Gst.init(None)

#First of all, build the pipeline
pipeline = Gst.parse_launch("playbin uri=//opt/crat/core/home/sounds/ATC/")


#start playing
pipeline.set_state(Gst.State.PLAYING)
print "Playing files..."

#get end of stream or its errors
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

#free resourses on pipeline
pipeline.set_state(Gst.State.NULL)


def _loop(self, message):
    self.player.set_property('uri', 'file://your_file_path')

player = gi.ElementFactory.make("playbin", "player")
player.connect("about-to-finish", self._loop)
player.set_property('uri', 'file://your_file_path')
