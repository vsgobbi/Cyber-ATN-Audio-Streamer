#!/usr/bin/env python

# Original file only for testings
# This is the client code for python-gstreamer.
# The gstreamer TCP/IP client sends a file
# through a tcpclientsink to a server on localhost


import gobject, pygst
from os.path import expanduser

pygst.require("0.10")


#from audioStreamPlayer import controller
import os, sys, random, fnmatch, thread, getopt, glob, time


# Setting GST_DEBUG_DUMP_DOT_DIR environment variable enables us to have a dotfile generated
#os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
#os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')
try:
    import gi
except:
    pass
try:
    import pygst
    pygst.require("0.10")
    import gst
except:
    pass


# create a pipeline and add [ filesrc ! tcpclientsink ]
pipeline = gst.Pipeline("client")

#player = gst.element_factory_make("playbin", "player")
src = gst.element_factory_make("filesrc", "source")

#create random heap to store mp3 files to our string...

#Sort .mp3 files randomly in our directory and check necessary conditions
#files = []


#select the current path and return it as a string
#path = os.getcwd()

src.set_property("location", "/opt/crat/core/home/sounds/ATC/303.mp3")


#add all elements to pipeline
pipeline.add(src)
#pipeline.add(player)

#set client properties and create pipeline
client = gst.element_factory_make("tcpclientsink", "client")
pipeline.add(client)
client.set_property("host", "0.0.0.0")
client.set_property("port", 3030)
src.link(client)


#check if pipeline and sources are okay
if (not pipeline or not src):
    print 'Client problem found... Not all elements could be created.'
    exit(-1)


pipeline.set_state(gst.STATE_PLAYING)
print 'Playing file...'


def printMsg():
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
                                 gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
    pipeline.set_new_stream_time(15)
    pipeline.set_state(gst.STATE_NULL)
    print msg

printMsg()


# create random list and play it in shuffle?
#bus = pipeline.set_bus()
# enter into a mainloop
#gobject.start_new_thread()
loop = gobject.MainLoop()
loop.run()


# NOTES:
# After a long time testing the codecs missing and searching for it.
# To consider playing .mp3 files, check if 'mad' element plugin is installed with gst0.10, install it with:
# apt-get install gstreamer0.10-fluendo-mp3


# Testing with gst-launch-0.10 terminal command
# gst-launch-0.10 tcpserversrc host=localhost port=3000 ! decodebin ! audioconvert ! alsasink
# gst-launch-0.10 filesrc location=/home/vitor/Music/Gorillaz_Feel_Good_Inc.mp3 ! tcpclientsink host=localhost port=3000

